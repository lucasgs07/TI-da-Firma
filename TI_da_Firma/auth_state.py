"""Estado de autenticação: login, restauração de sessão e logout local."""

import json
from datetime import datetime, timezone

import reflex as rx

from . import xano_client

PERFIS = {1: "Administrador", 2: "Gestor", 3: "Técnico", 4: "Funcionário"}


def _ticket_view(ticket: dict) -> dict[str, str]:
    """Reduz um chamado da API aos campos apresentados ao funcionário."""
    aliases = {
        "status_name": ("status_name", "status_nome"),
        "category_name": ("category_name", "categoria_nome"),
        "priority_name": ("priority_name", "prioridade_nome"),
    }
    fields = ("id", "titulo", "descricao")
    view = {field: str(ticket.get(field) or "") for field in fields}
    for target, keys in aliases.items():
        view[target] = next(
            (str(ticket[key]) for key in keys if ticket.get(key) is not None), ""
        )
    return view


def _technical_ticket_view(ticket: dict) -> dict[str, str]:
    view = _ticket_view(ticket)
    for field in ("requester_name", "solicitante_id", "responsavel_id", "responsible_name",
                  "solucao_final", "atualizado_em", "resolvido_em"):
        view[field] = str(ticket.get(field) or "")
    technicians = ticket.get("tecnicos") or []
    view["technician_names"] = ", ".join(
        str(t.get("name") or f"Técnico #{t.get('id')}") for t in technicians if isinstance(t, dict)
    ) or view["responsible_name"] or "Sem técnico associado"
    return view


def _interaction_view(row: dict) -> dict[str, str]:
    view = {key: str(row.get(key) or "") for key in ("id", "mensagem", "user_id", "author_name")}
    view["author_name"] = view["author_name"] or f"Usuário #{view['user_id']}"
    stamp = row.get("created_at")
    try:
        dt = (datetime.fromtimestamp(float(stamp) / 1000, timezone.utc)
              if isinstance(stamp, (int, float)) else datetime.fromisoformat(str(stamp).replace("Z", "+00:00")))
        view["data"] = dt.strftime("%d/%m/%Y %H:%M %z")
    except (ValueError, TypeError, OverflowError, OSError):
        view["data"] = str(stamp or "Data não informada")
    return view


class AuthState(rx.State):
    # Persistidos no LocalStorage do navegador (sobrevivem ao fechar o navegador).
    auth_token: str = rx.LocalStorage("", name="auth_token")
    perfil_json: str = rx.LocalStorage("", name="auth_perfil")

    # Estado efêmero de interface.
    autenticado: bool = False
    carregando: bool = False
    erro: str = ""
    erro_rede: bool = False
    chamados: list[dict[str, str]] = []
    categorias: list[dict[str, str]] = []
    prioridades: list[dict[str, str]] = []
    chamado_atual: dict[str, str] = {}
    tela_funcionario: str = "lista"
    erro_chamados: str = ""
    sucesso_chamado: str = ""
    carregando_chamados: bool = False
    carregando_opcoes: bool = False
    enviando_chamado: bool = False
    chamados_tecnicos: list[dict[str, str]] = []
    atendimento: dict[str, str] = {}
    historico: list[dict[str, str]] = []
    tecnicos_atendimento: list[dict[str, str]] = []
    tela_tecnico: str = "lista"
    erro_tecnico: str = ""
    erro_historico: str = ""
    sucesso_tecnico: str = ""
    carregando_tecnico: bool = False
    carregando_historico: bool = False
    enviando_atendimento: bool = False
    comentario: str = ""
    solucao: str = ""
    status_destino: str = ""

    @rx.event
    def set_comentario(self, value: str):
        if self._tecnico_autorizado() and not self.enviando_atendimento:
            self.comentario = value

    @rx.event
    def set_solucao(self, value: str):
        if self._tecnico_autorizado() and not self.enviando_atendimento:
            self.solucao = value

    @rx.event
    def set_status_destino(self, value: str):
        if self._tecnico_autorizado() and not self.enviando_atendimento:
            self.status_destino = value

    @rx.var
    def tecnico_associado(self) -> bool:
        actor_id = self.perfil.get("id", "")
        return bool(actor_id) and any(t.get("id") == actor_id for t in self.tecnicos_atendimento)

    @rx.var
    def pode_associar(self) -> bool:
        return self._tecnico_autorizado() and self.atendimento.get("status_name") == "Aberto" and not self.tecnico_associado

    @rx.var
    def pode_atualizar_atendimento(self) -> bool:
        return (self._tecnico_autorizado() and self.tecnico_associado
                and self.atendimento.get("status_name") in
                ("Aberto", "Em Análise", "Em atendimento", "Aguardando usuário"))

    def _tecnico_autorizado(self) -> bool:
        return self.autenticado and self._perfil_id() == 3

    def _limpar_atendimento(self) -> None:
        self.atendimento = {}
        self.historico = []
        self.tecnicos_atendimento = []
        self.comentario = ""
        self.solucao = ""
        self.status_destino = ""
        self.erro_tecnico = ""
        self.erro_historico = ""
        self.sucesso_tecnico = ""

    def _limpar_tecnico(self) -> None:
        self._limpar_atendimento()
        self.chamados_tecnicos = []
        self.tela_tecnico = "lista"
        self.carregando_tecnico = False
        self.carregando_historico = False
        self.enviando_atendimento = False

    def _erro_atendimento(self, exc: Exception) -> None:
        if isinstance(exc, xano_client.XanoRejected):
            self._invalidar_sessao_rejeitada()
        elif isinstance(exc, (xano_client.XanoOperationError, xano_client.XanoConfigError, ValueError)):
            self.erro_tecnico = str(exc)
        else:
            self.erro_tecnico = "Não foi possível concluir a consulta ou operação. Atualize para conferir o estado atual antes de tentar novamente."

    def _carregar_lista_tecnica(self) -> None:
        try:
            rows = xano_client.technician_tickets(self.auth_token)
            self.chamados_tecnicos = [_technical_ticket_view(row) for row in rows]
        except (xano_client.XanoConfigError, xano_client.XanoRejected,
                xano_client.XanoUnavailable, xano_client.XanoOperationError) as exc:
            self.chamados_tecnicos = []
            self._erro_atendimento(exc)

    def _carregar_atendimento(self, ticket_id: int) -> None:
        ticket = xano_client.technician_ticket(ticket_id, self.auth_token)
        self.atendimento = _technical_ticket_view(ticket)
        assignments = ticket.get("tecnicos")
        self.tecnicos_atendimento = [
            {"id": str(t.get("id") or ""), "name": str(t.get("name") or "")}
            for t in assignments or [] if isinstance(t, dict)
        ]
        if "tecnicos" not in ticket and ticket.get("responsavel_id"):
            self.tecnicos_atendimento = [{"id": str(ticket["responsavel_id"]),
                                          "name": str(ticket.get("responsible_name") or "") }]

    def _carregar_historico(self) -> None:
        self.historico = []
        self.erro_historico = ""
        if not self.atendimento.get("id"):
            return
        try:
            rows = xano_client.ticket_interactions(int(self.atendimento["id"]), self.auth_token)
            self.historico = [_interaction_view(row) for row in rows]
        except xano_client.XanoRejected:
            self._invalidar_sessao_rejeitada()
        except (xano_client.XanoConfigError, xano_client.XanoUnavailable, xano_client.XanoOperationError):
            self.erro_historico = "Não foi possível carregar o histórico. Tente novamente."

    @rx.event
    def atualizar_lista_tecnica(self):
        if not self._tecnico_autorizado() or self.enviando_atendimento:
            return
        self.erro_tecnico = ""
        self.carregando_tecnico = True
        yield
        self._carregar_lista_tecnica()
        self.carregando_tecnico = False
        if not self.autenticado:
            yield rx.redirect("/login")

    @rx.event
    def abrir_atendimento(self, chamado_id: str):
        if not self._tecnico_autorizado() or self.enviando_atendimento:
            return
        self._limpar_atendimento()
        self.tela_tecnico = "detalhe"
        self.carregando_tecnico = True
        yield
        try:
            ticket_id = int(chamado_id)
            if ticket_id < 1:
                raise ValueError("Identificador de chamado inválido.")
            self._carregar_atendimento(ticket_id)
            self.solucao = self.atendimento.get("solucao_final", "")
            current = self.atendimento.get("status_name", "")
            self.status_destino = current if current in xano_client.OPERATIONAL_STATUSES else "Em atendimento"
        except (ValueError, xano_client.XanoConfigError, xano_client.XanoRejected,
                xano_client.XanoUnavailable, xano_client.XanoOperationError) as exc:
            self._erro_atendimento(exc)
        self.carregando_tecnico = False
        if self.atendimento:
            self.carregando_historico = True
            yield
            self._carregar_historico()
            self.carregando_historico = False
        if not self.autenticado:
            yield rx.redirect("/login")

    @rx.event
    def atualizar_historico(self):
        if not self._tecnico_autorizado() or self.enviando_atendimento:
            return
        self.carregando_historico = True
        yield
        self._carregar_historico()
        self.carregando_historico = False
        if not self.autenticado:
            yield rx.redirect("/login")

    @rx.event
    def voltar_lista_tecnica(self):
        if not self._tecnico_autorizado() or self.enviando_atendimento:
            return
        self._limpar_atendimento()
        self.tela_tecnico = "lista"

    @rx.event
    def executar_atendimento(self, acao: str):
        if not self._tecnico_autorizado() or self.enviando_atendimento or not self.atendimento.get("id"):
            return
        self.erro_tecnico = ""
        self.sucesso_tecnico = ""
        if ((acao == "associar" and not self.pode_associar)
                or (acao == "comentar" and not self.tecnico_associado)
                or (acao == "status" and not self.pode_atualizar_atendimento)):
            self.erro_tecnico = "Ação indisponível para este chamado. Atualize para conferir suas permissões."
            return
        if acao not in ("associar", "comentar", "status"):
            return
        ticket_id = int(self.atendimento["id"])
        self.enviando_atendimento = True
        yield
        try:
            if acao == "associar":
                xano_client.claim_ticket(ticket_id, self.auth_token)
            elif acao == "comentar":
                xano_client.comment_ticket(ticket_id, self.comentario, self.auth_token)
                self.comentario = ""
            else:
                xano_client.update_ticket(ticket_id, self.status_destino, self.solucao, self.auth_token)
            self.sucesso_tecnico = "Operação salva com sucesso."
            # A resposta de escrita é reduzida; recarregar o contrato completo.
            try:
                self._carregar_atendimento(ticket_id)
                self._carregar_lista_tecnica()
                if self.autenticado:
                    self._carregar_historico()
            except (xano_client.XanoConfigError, xano_client.XanoRejected,
                    xano_client.XanoUnavailable, xano_client.XanoOperationError) as exc:
                self.atendimento = {}
                self.tecnicos_atendimento = []
                self._erro_atendimento(exc)
            if self.erro_tecnico:
                self.erro_tecnico = "Operação salva, mas os dados não puderam ser atualizados. Volte à lista e atualize."
        except (ValueError, xano_client.XanoConfigError, xano_client.XanoRejected,
                xano_client.XanoUnavailable, xano_client.XanoOperationError) as exc:
            self._erro_atendimento(exc)
        finally:
            self.enviando_atendimento = False
        if not self.autenticado:
            yield rx.redirect("/login")

    @rx.var
    def perfil(self) -> dict[str, str]:
        try:
            data = json.loads(self.perfil_json) if self.perfil_json else {}
        except ValueError:
            data = {}
        return {k: "" if v is None else str(v) for k, v in data.items()}

    @rx.var
    def nome_perfil(self) -> str:
        try:
            return PERFIS.get(int(self.perfil.get("perfil_id", "")), "Desconhecido")
        except ValueError:
            return "Desconhecido"

    @rx.var
    def nomes_categorias(self) -> list[str]:
        return [categoria["nome"] for categoria in self.categorias]

    @rx.var
    def nomes_prioridades(self) -> list[str]:
        return [prioridade["nome"] for prioridade in self.prioridades]

    @rx.var
    def possui_chamados(self) -> bool:
        return bool(self.chamados)

    @rx.var
    def opcoes_chamado_validas(self) -> bool:
        return (
            bool(self.categorias)
            and bool(self.prioridades)
            and not self.carregando_opcoes
        )

    def _perfil_id(self) -> int:
        try:
            return int(self.perfil.get("perfil_id", ""))
        except (TypeError, ValueError):
            return 0

    def _funcionario_autorizado(self) -> bool:
        return self.autenticado and self._perfil_id() == 4

    def _limpar_dados_chamados(self) -> None:
        self.chamados = []
        self.categorias = []
        self.prioridades = []
        self.chamado_atual = {}
        self.tela_funcionario = "lista"
        self.erro_chamados = ""
        self.sucesso_chamado = ""
        self.carregando_chamados = False
        self.carregando_opcoes = False
        self.enviando_chamado = False

    def _carregar_chamados(self) -> None:
        try:
            tickets = xano_client.list_tickets(self.auth_token)
        except xano_client.XanoConfigError as exc:
            self.erro_chamados = str(exc)
        except xano_client.XanoRejected:
            self._invalidar_sessao_rejeitada()
        except xano_client.XanoUnavailable:
            self.erro_chamados = "Não foi possível carregar seus chamados. Tente novamente."
        else:
            self.chamados = [_ticket_view(ticket) for ticket in tickets]

    def _carregar_opcoes_chamado(self) -> None:
        self.categorias = []
        self.prioridades = []
        try:
            categorias = xano_client.list_categories(self.auth_token)
            prioridades = xano_client.list_priorities(self.auth_token)
        except xano_client.XanoConfigError as exc:
            self.erro_chamados = str(exc)
        except xano_client.XanoRejected:
            self._invalidar_sessao_rejeitada()
        except xano_client.XanoUnavailable:
            self.erro_chamados = "Não foi possível carregar categorias e prioridades."
        else:
            self.categorias = categorias
            self.prioridades = prioridades
            if not categorias:
                self.erro_chamados = "Nenhuma categoria está configurada para chamados."
            elif not prioridades:
                self.erro_chamados = "Nenhuma prioridade está configurada para chamados."

    def _salvar_perfil(self, user: dict) -> None:
        self.perfil_json = json.dumps(user)

    def _limpar_sessao(self) -> None:
        self._limpar_office()
        self.auth_token = ""
        self.perfil_json = ""
        self.autenticado = False
        self._limpar_dados_chamados()
        self._limpar_tecnico()

    def _limpar_office(self) -> None:
        from .office_state import OfficeState
        office = self._get_root_state().substates.get(OfficeState.get_name())
        if office is not None:
            office.reset()

    def _invalidar_sessao_rejeitada(self) -> None:
        self._limpar_sessao()
        self.erro = "Sua sessão foi rejeitada. Entre novamente."
        self.erro_rede = True

    def get_auth_headers(self) -> dict[str, str]:
        """Cabeçalho para futuras chamadas autenticadas ao Xano."""
        return xano_client.auth_headers(self.auth_token)

    @rx.event
    def entrar(self, form_data: dict):
        email = str(form_data.get("email", "")).strip()
        senha = str(form_data.get("password", ""))
        self.erro = ""
        self.erro_rede = False
        if not email or not senha:
            self.erro = "Informe e-mail e senha."
            return
        self.carregando = True
        yield
        try:
            resultado = xano_client.login(email, senha)
        except xano_client.XanoConfigError as exc:
            self.erro = str(exc)
        except xano_client.XanoRejected:
            self.erro = "E-mail ou senha inválidos."
        except xano_client.XanoUnavailable:
            self.erro = "Não foi possível conectar ao servidor. Tente novamente."
        else:
            self.auth_token = resultado.auth_token
            self._salvar_perfil(resultado.user)
            self.autenticado = True
            self.carregando = False
            return rx.redirect("/")
        self.carregando = False

    @rx.event
    def verificar_sessao(self):
        """Guarda da página protegida: valida o token com auth/me."""
        self.erro = ""
        self.erro_rede = False
        self.autenticado = False
        self._limpar_office()
        self._limpar_dados_chamados()
        self._limpar_tecnico()
        if not self.auth_token:
            return rx.redirect("/login")
        self.carregando = True
        yield
        try:
            user = xano_client.me(self.auth_token)
        except xano_client.XanoRejected:
            self._limpar_sessao()
            self.carregando = False
            return rx.redirect("/login")
        except xano_client.XanoConfigError as exc:
            self.erro = str(exc)
            self.erro_rede = True
        except xano_client.XanoUnavailable:
            self.erro = "Não foi possível validar a sessão. Verifique a conexão."
            self.erro_rede = True
        else:
            self._salvar_perfil(user)
            self.autenticado = True
            if self._perfil_id() == 4:
                self.carregando_chamados = True
                yield
                self._carregar_chamados()
                self.carregando_chamados = False
            elif self._perfil_id() == 3:
                self.carregando_tecnico = True
                yield
                self._carregar_lista_tecnica()
                self.carregando_tecnico = False
                if not self.autenticado:
                    yield rx.redirect("/login")
        self.carregando = False

    @rx.event
    def atualizar_chamados(self):
        if not self._funcionario_autorizado():
            self.erro_chamados = "Acesso não autorizado."
            return
        self.erro_chamados = ""
        self.carregando_chamados = True
        yield
        self._carregar_chamados()
        self.carregando_chamados = False

    @rx.event
    def mostrar_formulario_chamado(self):
        if not self._funcionario_autorizado():
            self.erro_chamados = "Acesso não autorizado."
            return
        self.tela_funcionario = "formulario"
        self.chamado_atual = {}
        self.erro_chamados = ""
        self.sucesso_chamado = ""
        self.carregando_opcoes = True
        yield
        self._carregar_opcoes_chamado()
        self.carregando_opcoes = False

    @rx.event
    def ver_chamado(self, chamado_id: str):
        if not self._funcionario_autorizado():
            self.chamado_atual = {}
            self.erro_chamados = "Acesso não autorizado."
            return
        try:
            parsed_id = int(chamado_id)
        except (TypeError, ValueError):
            self.chamado_atual = {}
            self.erro_chamados = "Identificador de chamado inválido."
            return
        if parsed_id < 1:
            self.chamado_atual = {}
            self.erro_chamados = "Identificador de chamado inválido."
            return
        self.chamado_atual = {}
        self.erro_chamados = ""
        self.tela_funcionario = "detalhe"
        self.carregando_chamados = True
        yield
        try:
            ticket = xano_client.get_ticket(parsed_id, self.auth_token)
        except xano_client.XanoConfigError as exc:
            self.erro_chamados = str(exc)
        except xano_client.XanoRejected:
            self._invalidar_sessao_rejeitada()
        except xano_client.XanoUnavailable:
            self.erro_chamados = (
                "Não foi possível carregar este chamado. Ele pode não existir "
                "ou não estar disponível para sua conta."
            )
        else:
            self.chamado_atual = _ticket_view(ticket)
        self.carregando_chamados = False

    @rx.event
    def voltar_para_chamados(self):
        if not self._funcionario_autorizado():
            self.erro_chamados = "Acesso não autorizado."
            return
        self.tela_funcionario = "lista"
        self.chamado_atual = {}
        self.erro_chamados = ""

    @rx.event
    def abrir_chamado(self, form_data: dict):
        if not self._funcionario_autorizado():
            self.erro_chamados = "Acesso não autorizado."
            return
        titulo = str(form_data.get("titulo", "")).strip()
        descricao = str(form_data.get("descricao", "")).strip()
        categoria_nome = str(form_data.get("categoria", "")).strip()
        prioridade_nome = str(form_data.get("prioridade", "")).strip()
        categorias = {item["nome"]: item["id"] for item in self.categorias}
        prioridades = {item["nome"]: item["id"] for item in self.prioridades}
        if not titulo or not descricao or categoria_nome not in categorias or prioridade_nome not in prioridades:
            self.erro_chamados = "Preencha título, descrição, categoria e prioridade válidos."
            return
        if self.enviando_chamado:
            return
        self.erro_chamados = ""
        self.sucesso_chamado = ""
        self.enviando_chamado = True
        yield
        try:
            created = xano_client.create_ticket(
                titulo,
                descricao,
                int(categorias[categoria_nome]),
                int(prioridades[prioridade_nome]),
                self.auth_token,
            )
        except xano_client.XanoConfigError as exc:
            self.erro_chamados = str(exc)
        except xano_client.XanoRejected:
            self._invalidar_sessao_rejeitada()
        except xano_client.XanoUnavailable:
            self.erro_chamados = "Não foi possível abrir o chamado. Revise os dados e tente novamente."
        else:
            ticket_id = str(created.get("id") or "")
            self.sucesso_chamado = (
                f"Chamado #{ticket_id} aberto com sucesso."
                if ticket_id
                else "Chamado aberto com sucesso."
            )
            self.tela_funcionario = "lista"
            self.carregando_chamados = True
            yield
            self._carregar_chamados()
            if self.erro_chamados:
                self.erro_chamados = (
                    "Chamado criado, mas a lista não pôde ser atualizada. "
                    "Use Atualizar para tentar novamente."
                )
        self.carregando_chamados = False
        self.enviando_chamado = False

    @rx.event
    def verificar_login(self):
        """Na tela de login, quem já tem token segue para a home (que valida)."""
        if self.auth_token:
            return rx.redirect("/")

    @rx.event
    def sair(self):
        """Logout local: o token no Xano continua válido até expirar (até 24h)."""
        self._limpar_sessao()
        self.erro = ""
        return rx.redirect("/login")
