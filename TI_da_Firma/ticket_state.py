"""Estado do formulário de abertura de chamados."""

import reflex as rx

from . import xano_client
from .auth_state import AuthState

STATUS_OPERACIONAIS = [
    "Aberto",
    "Em Análise",
    "Em atendimento",
    "Aguardando usuário",
    "Resolvido",
    "Fechado",
]


def _options_rejection(status_code: int) -> tuple[bool, str]:
    if status_code == 401:
        return True, "A sessão expirou. Entre novamente para carregar as opções."
    if status_code == 403:
        return False, "O Xano negou acesso às categorias ou prioridades; a sessão foi mantida."
    return False, "O Xano rejeitou a consulta de categorias ou prioridades."


def _missing_options_message(
    categorias: list[dict], prioridades: list[dict]
) -> str:
    if not categorias and not prioridades:
        return "Não há categorias nem prioridades cadastradas no Xano. Peça a um administrador para cadastrar esses valores."
    if not categorias:
        return "Não há categorias cadastradas no Xano. Peça a um administrador para cadastrar categorias."
    if not prioridades:
        return "Não há prioridades cadastradas no Xano. Peça a um administrador para cadastrar prioridades."
    return ""


class TicketState(AuthState):
    categorias: list[dict[str, str]] = []
    prioridades: list[dict[str, str]] = []
    categoria_chamado_id: str = ""
    prioridade_id: str = ""
    carregando_opcoes: bool = False
    enviando_chamado: bool = False
    erro_chamado: str = ""
    chamado_criado_id: str = ""
    chamado_criado_solicitante: str = ""
    chamado_criado_status: str = ""
    chamados: list[dict[str, str]] = []
    interacoes: list[dict[str, str]] = []
    status_operacionais: list[str] = STATUS_OPERACIONAIS
    chamado_selecionado_id: str = ""
    status_atualizacao: str = ""
    carregando_chamados: bool = False
    operacao_chamado_em_andamento: bool = False
    erro_lista_chamados: str = ""
    erro_operacao_chamado: str = ""

    @rx.var
    def tem_opcoes_chamado(self) -> bool:
        return bool(self.categorias and self.prioridades)

    @rx.var
    def chamado_selecionado(self) -> dict[str, str]:
        for chamado in self.chamados:
            if chamado["id"] == self.chamado_selecionado_id:
                return chamado
        return {}

    @rx.var
    def interacoes_do_chamado(self) -> list[dict[str, str]]:
        return [
            interacao
            for interacao in self.interacoes
            if interacao["chamado_id"] == self.chamado_selecionado_id
        ]

    @rx.var
    def pode_assumir_chamado_selecionado(self) -> bool:
        try:
            eh_tecnico = int(self.perfil.get("perfil_id", "")) == 3
            user_id = self.perfil.get("id", "")
        except ValueError:
            return False
        ids_tecnicos = self.chamado_selecionado.get("tecnicos_ids", "").split(",")
        return (
            eh_tecnico
            and self.chamado_selecionado.get("status_nome") == "Aberto"
            and user_id not in ids_tecnicos
        )

    @rx.var
    def pode_atualizar_chamado_selecionado(self) -> bool:
        try:
            eh_tecnico = int(self.perfil.get("perfil_id", "")) == 3
            user_id = self.perfil.get("id", "")
        except ValueError:
            return False
        chamado = self.chamado_selecionado
        ids_tecnicos = chamado.get("tecnicos_ids", "").split(",")
        if ids_tecnicos == [""]:
            return eh_tecnico and chamado.get("responsavel_id") == user_id
        return eh_tecnico and user_id in ids_tecnicos

    @rx.var
    def pode_responder_chamado_selecionado(self) -> bool:
        try:
            perfil_id = int(self.perfil.get("perfil_id", ""))
        except ValueError:
            return False
        chamado = self.chamado_selecionado
        user_id = self.perfil.get("id", "")
        if perfil_id in (2, 4) and chamado.get("solicitante_id") == user_id:
            return True
        ids_tecnicos = chamado.get("tecnicos_ids", "").split(",")
        if perfil_id == 3 and user_id in ids_tecnicos:
            return True
        return perfil_id == 3 and not any(ids_tecnicos) and chamado.get("responsavel_id") == user_id

    @rx.event
    def selecionar_categoria(self, categoria_id: str):
        self.categoria_chamado_id = categoria_id

    @rx.event
    def selecionar_prioridade(self, prioridade_id: str):
        self.prioridade_id = prioridade_id

    @rx.event
    def selecionar_status_atualizacao(self, status_nome: str):
        self.status_atualizacao = status_nome

    @rx.event
    def selecionar_chamado(self, chamado_id: str):
        self.chamado_selecionado_id = chamado_id
        self.erro_operacao_chamado = ""
        for chamado in self.chamados:
            if chamado["id"] == chamado_id:
                self.status_atualizacao = chamado["status_nome"]
                break

    @rx.event
    def voltar_para_lista_chamados(self):
        self.chamado_selecionado_id = ""
        self.erro_operacao_chamado = ""

    @rx.event
    def carregar_chamados(self):
        self.erro_lista_chamados = ""
        if not self.auth_token:
            return rx.redirect("/login")
        self.carregando_chamados = True
        yield
        try:
            chamados = xano_client.get_tickets(self.auth_token)
            interacoes = xano_client.get_ticket_interactions(self.auth_token)
        except xano_client.XanoConfigError as exc:
            self.erro_lista_chamados = str(exc)
        except xano_client.XanoRejected:
            self.erro_lista_chamados = "Sua sessão não foi aceita ou seu perfil não pode consultar chamados."
        except xano_client.XanoUnavailable:
            self.erro_lista_chamados = "Não foi possível carregar os chamados. Verifique a conexão e tente novamente."
        else:
            ticket_fields = (
                "id",
                "titulo",
                "descricao",
                "solucao_final",
                "categoria_chamado_id",
                "category_name",
                "prioridade_id",
                "priority_name",
                "status_chamado_id",
                "status_name",
                "solicitante_id",
                "requester_name",
                "responsavel_id",
                "responsible_name",
            )
            self.chamados = []
            for ticket in chamados:
                normalized = {
                    field: str(ticket.get(field) or "") for field in ticket_fields
                }
                normalized["status_nome"] = normalized.pop("status_name")
                normalized["tecnicos_ids"] = ",".join(
                    str(technician.get("id", ""))
                    for technician in ticket.get("tecnicos", [])
                    if isinstance(technician, dict)
                )
                self.chamados.append(normalized)
            self.interacoes = [
                {
                    field: str(interaction.get(field) or "")
                    for field in ("id", "created_at", "mensagem", "chamado_id", "user_id")
                }
                for interaction in interacoes
            ]
        self.carregando_chamados = False

    @rx.event
    def assumir_chamado_selecionado(self):
        if self.operacao_chamado_em_andamento:
            return
        try:
            ticket_id = int(self.chamado_selecionado_id)
        except ValueError:
            self.erro_operacao_chamado = "Selecione um chamado válido."
            return
        self.erro_operacao_chamado = ""
        self.operacao_chamado_em_andamento = True
        yield
        try:
            xano_client.assume_ticket(self.auth_token, ticket_id)
        except xano_client.XanoConfigError as exc:
            self.erro_operacao_chamado = str(exc)
        except xano_client.XanoRejected:
            self.erro_operacao_chamado = "O Xano não autorizou a atribuição deste chamado."
        except xano_client.XanoUnavailable:
            self.erro_operacao_chamado = "Não foi possível assumir o chamado. Tente novamente."
        else:
            self.operacao_chamado_em_andamento = False
            return rx.redirect("/chamados")
        self.operacao_chamado_em_andamento = False

    @rx.event
    def atualizar_chamado(self, form_data: dict):
        if self.operacao_chamado_em_andamento:
            return
        status_nome = str(form_data.get("status_nome", "")).strip()
        solucao_final = str(form_data.get("solucao_final", "")).strip()
        if status_nome not in STATUS_OPERACIONAIS:
            self.erro_operacao_chamado = "Selecione um status válido."
            return
        if status_nome in ("Resolvido", "Fechado") and not solucao_final:
            self.erro_operacao_chamado = "Informe a solução final para resolver ou fechar o chamado."
            return
        try:
            ticket_id = int(self.chamado_selecionado_id)
        except ValueError:
            self.erro_operacao_chamado = "Selecione um chamado válido."
            return

        self.erro_operacao_chamado = ""
        self.operacao_chamado_em_andamento = True
        yield
        try:
            xano_client.update_ticket(
                self.auth_token,
                ticket_id,
                status_nome=status_nome,
                solucao_final=solucao_final if solucao_final else None,
            )
        except xano_client.XanoConfigError as exc:
            self.erro_operacao_chamado = str(exc)
        except xano_client.XanoRejected:
            self.erro_operacao_chamado = "O Xano rejeitou a atualização do chamado. Confira o status e tente novamente."
        except xano_client.XanoUnavailable:
            self.erro_operacao_chamado = "Não foi possível atualizar o chamado. Tente novamente."
        else:
            self.chamados = [
                {
                    **ticket,
                    "status_nome": status_nome,
                    "solucao_final": solucao_final or ticket["solucao_final"],
                }
                if ticket["id"] == self.chamado_selecionado_id
                else ticket
                for ticket in self.chamados
            ]
            self.status_atualizacao = status_nome
        self.operacao_chamado_em_andamento = False

    @rx.event
    def registrar_interacao(self, form_data: dict):
        if self.operacao_chamado_em_andamento:
            return
        mensagem = str(form_data.get("mensagem", "")).strip()
        if not mensagem:
            self.erro_operacao_chamado = "Informe uma mensagem para registrar a interação."
            return
        try:
            ticket_id = int(self.chamado_selecionado_id)
        except ValueError:
            self.erro_operacao_chamado = "Selecione um chamado válido."
            return

        self.erro_operacao_chamado = ""
        self.operacao_chamado_em_andamento = True
        yield
        try:
            interaction = xano_client.create_ticket_interaction(
                self.auth_token,
                ticket_id,
                mensagem,
            )
        except xano_client.XanoConfigError as exc:
            self.erro_operacao_chamado = str(exc)
        except xano_client.XanoRejected:
            self.erro_operacao_chamado = "O Xano não autorizou esta interação para seu perfil."
        except xano_client.XanoUnavailable:
            self.erro_operacao_chamado = "Não foi possível registrar a interação. Tente novamente."
        else:
            self.interacoes = [
                *self.interacoes,
                {
                    "id": str(interaction.get("id", "")),
                    "created_at": str(interaction.get("created_at", "")),
                    "mensagem": str(interaction.get("mensagem", mensagem)),
                    "chamado_id": str(interaction.get("chamado_id", ticket_id)),
                    "user_id": str(interaction.get("user_id", self.perfil.get("id", ""))),
                },
            ]
        self.operacao_chamado_em_andamento = False

    @rx.event
    def carregar_opcoes_chamado(self):
        self.erro_chamado = ""
        self.erro_rede = False
        self.categorias = []
        self.prioridades = []
        if not self.auth_token:
            return rx.redirect("/login")

        self.carregando_opcoes = True
        yield
        try:
            perfil = xano_client.me(self.auth_token)
        except xano_client.XanoConfigError as exc:
            self.erro_chamado = str(exc)
            self.erro_rede = True
            self.carregando_opcoes = False
            return
        except xano_client.XanoRejected as exc:
            if exc.status_code in (401, 403):
                self._limpar_sessao()
                self.carregando_opcoes = False
                return rx.redirect("/login")
            self.erro_chamado = "Não foi possível validar a sessão no Xano."
            self.erro_rede = True
            self.carregando_opcoes = False
            return
        except xano_client.XanoUnavailable:
            self.erro_chamado = "Não foi possível validar a sessão. Verifique a conexão e tente novamente."
            self.erro_rede = True
            self.carregando_opcoes = False
            return

        self._salvar_perfil(perfil)
        self.autenticado = True
        if not self.pode_criar_chamado:
            self.erro_chamado = "Seu perfil não tem permissão para abrir chamados."
            self.carregando_opcoes = False
            return

        try:
            categorias = xano_client.get_ticket_categories(self.auth_token)
            prioridades = xano_client.get_ticket_priorities(self.auth_token)
        except xano_client.XanoConfigError as exc:
            self.erro_chamado = str(exc)
        except xano_client.XanoRejected as exc:
            limpar_sessao, mensagem = _options_rejection(exc.status_code)
            self.erro_chamado = mensagem
            if limpar_sessao:
                self._limpar_sessao()
                self.carregando_opcoes = False
                return rx.redirect("/login")
        except xano_client.XanoUnavailable:
            self.erro_chamado = "Não foi possível carregar as opções. Verifique a conexão e tente novamente."
        else:
            self.categorias = [
                {"id": str(item["id"]), "nome": str(item["nome"])}
                for item in categorias
            ]
            self.prioridades = [
                {"id": str(item["id"]), "nome": str(item["nome"])}
                for item in prioridades
            ]
            self.erro_chamado = _missing_options_message(categorias, prioridades)
        self.carregando_opcoes = False

    @rx.event
    def criar_chamado(self, form_data: dict):
        if self.enviando_chamado:
            return
        self.erro_chamado = ""
        titulo = str(form_data.get("titulo", "")).strip()
        descricao = str(form_data.get("descricao", "")).strip()
        categoria_id = str(form_data.get("categoria_chamado_id", ""))
        prioridade_id = str(form_data.get("prioridade_id", ""))

        if not 1 <= len(titulo) <= 200:
            self.erro_chamado = "Informe um título com até 200 caracteres."
            return
        if not 1 <= len(descricao) <= 10000:
            self.erro_chamado = "Informe uma descrição com até 10000 caracteres."
            return
        if categoria_id not in {item["id"] for item in self.categorias}:
            self.erro_chamado = "Selecione uma categoria válida."
            return
        if prioridade_id not in {item["id"] for item in self.prioridades}:
            self.erro_chamado = "Selecione uma prioridade válida."
            return

        self.enviando_chamado = True
        yield
        try:
            chamado = xano_client.create_ticket(
                self.auth_token,
                titulo=titulo,
                descricao=descricao,
                categoria_chamado_id=int(categoria_id),
                prioridade_id=int(prioridade_id),
            )
        except xano_client.XanoConfigError as exc:
            self.erro_chamado = str(exc)
        except xano_client.XanoRejected:
            self.erro_chamado = "O Xano rejeitou o chamado. Confira os dados e tente novamente."
        except xano_client.XanoUnavailable:
            self.erro_chamado = "Não foi possível confirmar a criação do chamado. Tente novamente."
        else:
            self.chamado_criado_id = str(chamado.get("id", ""))
            self.chamado_criado_solicitante = str(
                chamado.get("solicitante_nome") or self.perfil.get("name", "")
            )
            self.chamado_criado_status = str(chamado.get("status_nome", ""))
        self.enviando_chamado = False