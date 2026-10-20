"""Aplicação de gestão interna: login, home protegida e logout."""

import reflex as rx

from .auth_state import AuthState
from .technician_portal import technician_portal


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
        rx.hstack(
            rx.heading("Meus chamados", size="5"),
            rx.spacer(),
            rx.button(
                "Atualizar",
                on_click=AuthState.atualizar_chamados,
                loading=AuthState.carregando_chamados,
                variant="soft",
            ),
            rx.button(
                "Abrir chamado",
                on_click=AuthState.mostrar_formulario_chamado,
            ),
            width="100%",
            align="center",
        ),
        rx.cond(
            AuthState.carregando_chamados,
            rx.center(rx.spinner(), padding="2rem"),
            rx.cond(
                AuthState.erro_chamados != "",
                rx.text(""),
                rx.cond(
                    AuthState.possui_chamados,
                    rx.vstack(
                        rx.foreach(AuthState.chamados, _ticket_card),
                        width="100%",
                        spacing="3",
                    ),
                    rx.callout(
                        "Você ainda não abriu chamados. Use “Abrir chamado” para registrar uma solicitação.",
                        color_scheme="gray",
                    ),
                ),
            ),
        ),
        width="100%",
        spacing="4",
    )


def _ticket_form() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.button(
                "Voltar",
                on_click=AuthState.voltar_para_chamados,
                variant="soft",
            ),
            rx.heading("Abrir chamado", size="5"),
            width="100%",
            align="center",
        ),
        rx.cond(
            AuthState.carregando_opcoes,
            rx.center(rx.spinner(), padding="1rem"),
            rx.form(
                rx.vstack(
                    rx.input(
                        name="titulo",
                        placeholder="Título do chamado",
                        max_length=200,
                        required=True,
                        width="100%",
                    ),
                    rx.text_area(
                        name="descricao",
                        placeholder="Descreva o problema ou solicitação",
                        max_length=10000,
                        required=True,
                        width="100%",
                    ),
                    rx.select(
                        AuthState.nomes_categorias,
                        name="categoria",
                        placeholder="Selecione uma categoria",
                        required=True,
                        width="100%",
                    ),
                    rx.select(
                        AuthState.nomes_prioridades,
                        name="prioridade",
                        placeholder="Selecione uma prioridade",
                        required=True,
                        width="100%",
                    ),
                    rx.button(
                        "Registrar chamado",
                        type="submit",
                        loading=AuthState.enviando_chamado,
                        disabled=~AuthState.opcoes_chamado_validas,
                        width="100%",
                    ),
                    width="100%",
                    spacing="3",
                ),
                on_submit=AuthState.abrir_chamado,
                reset_on_submit=False,
                width="100%",
            ),
        ),
        width="100%",
        spacing="4",
    )


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
    return rx.center(
        rx.card(
            rx.form(
                rx.vstack(
                    rx.heading("Entrar", size="6"),
                    rx.input(name="email", type="email", placeholder="E-mail", width="100%"),
                    rx.input(
                        name="password",
                        type="password",
                        placeholder="Senha",
                        width="100%",
                    ),
                    rx.cond(
                        AuthState.erro != "",
                        rx.callout(AuthState.erro, color_scheme="red", width="100%"),
                    ),
                    rx.button(
                        "Entrar",
                        type="submit",
                        loading=AuthState.carregando,
                        width="100%",
                    ),
                    spacing="3",
                ),
                on_submit=AuthState.entrar,
            ),
            width="22rem",
        ),
        min_height="100vh",
    )


def home_page() -> rx.Component:
    generic_home = rx.vstack(
        rx.text("Olá, ", AuthState.perfil["name"], size="5"),
        rx.text("Perfil: ", AuthState.nome_perfil),
        rx.callout(
            "O logout encerra a sessão apenas neste navegador; o token pode "
            "permanecer válido no servidor por até 24 horas.",
            color_scheme="gray",
        ),
        spacing="4",
        padding_y="2rem",
    )
    return rx.container(
        rx.cond(
            AuthState.autenticado,
            rx.vstack(
                rx.hstack(
                    rx.heading("TI da Firma", size="6"),
                    rx.spacer(),
                    rx.button("Sair", on_click=AuthState.sair, variant="soft"),
                    width="100%",
                    align="center",
                ),
                rx.cond(
                    AuthState.perfil["perfil_id"] == "4",
                    _employee_portal(),
                    rx.cond(AuthState.perfil["perfil_id"] == "3", technician_portal(), generic_home),
                ),
                spacing="4",
                padding_y="2rem",
            ),
            rx.center(
                rx.cond(
                    AuthState.erro_rede,
                    rx.vstack(
                        rx.callout(AuthState.erro, color_scheme="red"),
                        rx.button("Tentar novamente", on_click=AuthState.verificar_sessao),
                        rx.button("Sair", on_click=AuthState.sair, variant="soft"),
                    ),
                    rx.spinner(),
                ),
                min_height="80vh",
            ),
        ),
    )


app = rx.App()
app.add_page(home_page, route="/", on_load=AuthState.verificar_sessao)
app.add_page(login_page, route="/login", on_load=AuthState.verificar_login)
