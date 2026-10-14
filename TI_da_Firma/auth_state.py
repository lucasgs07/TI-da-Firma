"""Estado de autenticação: login, restauração de sessão e logout local."""

import json

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
        self.auth_token = ""
        self.perfil_json = ""
        self.autenticado = False
        self._limpar_dados_chamados()

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
