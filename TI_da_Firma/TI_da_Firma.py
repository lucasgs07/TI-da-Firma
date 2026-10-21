"""Aplicação de gestão interna: login, home protegida e logout."""

import reflex as rx

from .auth_state import AuthState
from .technician_portal import technician_portal
from .office_portal import office_portal
from .office_state import OfficeState
from .admin_portal import admin_portal
from .admin_state import AdminState
from . import design as ui
from .shell import workspace
from .ticket_filters import TicketFilters, ticket_filters, ticket_results


def _ticket_card(ticket: rx.Var[dict[str, str]]) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.vstack(
                rx.heading(ticket["titulo"], size="4"),
                rx.text("Status: ", ticket["status_name"]),
                rx.text("Categoria: ", ticket["category_name"]),
                rx.text("Prioridade: ", ticket["priority_name"]),
                align="start",
                spacing="1",
            ),
            rx.spacer(),
            rx.button(
                "Ver detalhes",
                on_click=lambda: AuthState.ver_chamado(ticket["id"]),
                variant="soft",
            ),
            width="100%",
            align="center",
        ),
        width="100%",
    )


def _ticket_list() -> rx.Component:
    return rx.vstack(
        ui.heading("Meus chamados", "Pesquise e acompanhe somente as solicitações que você abriu.",
            rx.button("+ Abrir chamado", on_click=AuthState.mostrar_formulario_chamado)),
        ticket_filters(), ticket_results(AuthState.lista_visual_chamados, "Somente meus chamados"),
        rx.cond(
            AuthState.carregando_chamados,
            rx.center(rx.spinner(), padding="2rem"),
            rx.cond(
                AuthState.erro_chamados != "",
                rx.text(""),
                rx.cond(
                    AuthState.possui_chamados,
                    rx.cond(AuthState.lista_visual_chamados.length() > 0,
                        ui.ticket_table(AuthState.lista_visual_chamados, AuthState.ver_chamado, "requester_name", "Solicitante", AuthState.perfil.get("name", "")),
                        ui.empty("Nenhum resultado", "Ajuste a busca ou o filtro de status.")),
                    ui.empty("Nenhum chamado por aqui", "Quando precisar da equipe de T.I., abra sua primeira solicitação.",
                             rx.button("Abrir chamado", on_click=AuthState.mostrar_formulario_chamado)),
                ),
            ),
        ),
        rx.text("Você visualiza somente os chamados que abriu. Indicadores dos registros carregados.", font_size="12px", color=ui.MUTED),
        width="100%",
        spacing="5",
    )


def _ticket_form() -> rx.Component:
    return rx.vstack(
        ui.heading("Abrir chamado", "Conte o que aconteceu para a equipe entender sua solicitação."),
        rx.box(
            ui.panel(
                rx.heading("Sobre o que você precisa?", size="4", margin_bottom="20px"),
                rx.cond(AuthState.carregando_opcoes, rx.spinner(),
                    rx.form(rx.vstack(
                        ui.field("Título *", rx.input(name="titulo", placeholder="Ex.: não consigo imprimir no financeiro",
                            aria_label="Título", required=True, max_length=200, width="100%")),
                        ui.field("Descrição *", rx.text_area(name="descricao", required=True, max_length=10000,
                            aria_label="Descrição", placeholder="Descreva o problema, quando começou e como ele afeta seu trabalho.", width="100%")),
                        rx.box(
                            ui.field("Categoria *", rx.select(AuthState.nomes_categorias, name="categoria", placeholder="Selecione uma categoria",
                                aria_label="Categoria", required=True, width="100%")),
                            ui.field("Prioridade *", rx.select(AuthState.nomes_prioridades, name="prioridade", placeholder="Selecione uma prioridade",
                                aria_label="Prioridade", required=True, width="100%")), class_name="nexo-pair"),
                        rx.flex(rx.button("Enviar chamado", type="submit", loading=AuthState.enviando_chamado,
                                          disabled=~AuthState.opcoes_chamado_validas),
                                rx.button("Cancelar", on_click=AuthState.voltar_para_chamados, type="button", variant="outline",
                                          disabled=AuthState.enviando_chamado), gap="3", wrap="wrap"),
                        align="start", spacing="5", width="100%"), on_submit=AuthState.abrir_chamado,
                        reset_on_submit=False, width="100%"))),
            ui.panel(rx.vstack(rx.heading("Um bom relato ajuda muito", size="4"),
                rx.text("1. Diga o que você tentou fazer.", color=ui.MUTED),
                rx.text("2. Explique o que aconteceu.", color=ui.MUTED),
                rx.text("3. Informe qual equipamento está usando.", color=ui.MUTED),
                ui.notice("As opções de categoria e prioridade seguem a configuração da empresa."),
                spacing="5", align="start")), class_name="nexo-form-columns"),
        width="100%", spacing="5")


def _ticket_detail() -> rx.Component:
    return rx.vstack(
        rx.button(
            "Voltar aos chamados",
            on_click=AuthState.voltar_para_chamados,
            variant="soft",
            align_self="start",
        ),
        rx.cond(
            AuthState.carregando_chamados,
            rx.center(rx.spinner(), padding="2rem"),
            rx.cond(
                AuthState.erro_chamados == "",
                rx.card(
                    rx.vstack(
                        rx.heading(AuthState.chamado_atual["titulo"], size="5"),
                        rx.text("Descrição: ", AuthState.chamado_atual["descricao"]),
                        rx.text("Status: ", AuthState.chamado_atual["status_name"]),
                        rx.text(
                            "Categoria: ", AuthState.chamado_atual["category_name"]
                        ),
                        rx.text(
                            "Prioridade: ", AuthState.chamado_atual["priority_name"]
                        ),
                        align="start",
                        spacing="3",
                        width="100%",
                    ),
                    width="100%",
                ),
                rx.text(""),
            ),
        ),
        width="100%",
        spacing="4",
    )


def _employee_portal() -> rx.Component:
    return rx.vstack(
        rx.cond(
            AuthState.erro_chamados != "",
            rx.callout(AuthState.erro_chamados, color_scheme="red", width="100%"),
        ),
        rx.cond(
            AuthState.sucesso_chamado != "",
            rx.callout(AuthState.sucesso_chamado, color_scheme="green", width="100%"),
        ),
        rx.cond(
            AuthState.tela_funcionario == "formulario",
            _ticket_form(),
            rx.cond(
                AuthState.tela_funcionario == "detalhe",
                _ticket_detail(),
                _ticket_list(),
            ),
        ),
        width="100%",
        spacing="4",
    )


def login_page() -> rx.Component:
    return rx.box(
        rx.box(rx.box(
            rx.text("Nexo", font_size="28px", weight="bold"),
            rx.box(class_name="nexo-login-spacer"),
            rx.heading("Menos ruído.", rx.el.br(), "Mais solução.", font_size="32px", line_height="1.45"),
            rx.text("Pessoas, chamados e tarefas no mesmo lugar.", rx.el.br(),
                    "Seu trabalho flui melhor quando tudo se conecta.", color="#b8ccc6", class_name="nexo-login-story-description"),
            rx.box(rx.vstack(rx.text("DO PEDIDO À SOLUÇÃO", font_size="12px"),
                rx.text("Impressora do financeiro offline", font_size="18px", weight="bold"),
                rx.text("#1048 · Em atendimento"), rx.text("Lucas e Pedro estão cuidando disso.", font_size="12px"),
                spacing="5", align="start"), class_name="nexo-login-card", aria_label="Exemplo ilustrativo de atendimento"),
            rx.text("Uma central para toda a firma.", color="#b8ccc6", font_size="12px", class_name="nexo-login-story-caption"),
            class_name="nexo-login-story-content"), class_name="nexo-login-story"),
        rx.box(rx.vstack(
            rx.text("BEM-VINDO DE VOLTA", color=ui.BRAND, font_size="12px"),
            rx.heading("Entre no seu workspace", font_size="28px", font_weight="600", line_height="1.45"),
            rx.text("Use suas credenciais corporativas.", color=ui.MUTED),
            rx.form(rx.vstack(
                ui.field("E-mail", rx.input(name="email", type="email", placeholder="voce@empresa.com.br", required=True,
                         aria_label="E-mail", auto_complete=True, width="100%", disabled=AuthState.carregando)),
                ui.field("Senha", rx.input(name="password", type="password", placeholder="••••••••", required=True,
                         aria_label="Senha", auto_complete=True, width="100%", disabled=AuthState.carregando)),
                rx.cond(AuthState.erro != "", rx.callout(AuthState.erro, color_scheme="red", width="100%")),
                rx.button("Entrar", type="submit", loading=AuthState.carregando, width="100%"),
                align="start", spacing="5", width="100%"), on_submit=AuthState.entrar, reset_on_submit=False, width="100%"),
            rx.text("Precisa de acesso? Fale com o administrador.", font_size="12px", color=ui.MUTED),
            rx.text("Sua área é definida automaticamente pelo seu perfil.", font_size="12px", color=ui.MUTED),
            align="start", spacing="5", width="100%"), class_name="nexo-login-form"), class_name="nexo-login")


def _session_pending() -> rx.Component:
    return rx.center(rx.cond(AuthState.erro_rede,
        rx.vstack(rx.callout(AuthState.erro, color_scheme="red"),
                  rx.button("Tentar novamente", on_click=AuthState.verificar_sessao),
                  rx.button("Sair", on_click=AuthState.sair, variant="soft")), rx.spinner()),
        class_name="nexo-loading")


def tasks_page() -> rx.Component:
    return rx.cond(AuthState.autenticado,
        workspace(rx.cond((AuthState.perfil["perfil_id"] == "3") | (AuthState.perfil["perfil_id"] == "4"),
            office_portal(employee=True),
            rx.callout("Esta tela é exclusiva para técnicos e funcionários.", color_scheme="red")), tasks=True),
        _session_pending())


def home_page() -> rx.Component:
    return rx.cond(AuthState.autenticado,
        workspace(rx.cond(AuthState.perfil["perfil_id"] == "4", _employee_portal(),
            rx.cond(AuthState.perfil["perfil_id"] == "3", technician_portal(),
                rx.cond(AuthState.perfil["perfil_id"] == "2", office_portal(),
                    rx.cond(AuthState.perfil["perfil_id"] == "1", admin_portal(),
                        rx.callout("Perfil não reconhecido. Entre em contato com o administrador.", color_scheme="red")))))),
        _session_pending())


app = rx.App(style=ui.APP_STYLE, stylesheets=["/nexo.css"])
app.add_page(home_page, route="/", title="Nexo | Workspace", on_load=[AuthState.verificar_sessao, OfficeState.initialize, AdminState.initialize, TicketFilters.initialize])
app.add_page(tasks_page, route="/tarefas", title="Nexo | Minhas tarefas", on_load=[AuthState.verificar_sessao, OfficeState.initialize])
app.add_page(login_page, route="/login", title="Nexo | Entrar", on_load=AuthState.verificar_login)
