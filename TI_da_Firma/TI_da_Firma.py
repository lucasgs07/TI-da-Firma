"""Aplicação de gestão interna: login, home protegida e logout."""

import reflex as rx

from .auth_state import AuthState


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
                rx.text("Olá, ", AuthState.perfil["name"], size="5"),
                rx.text("Perfil: ", AuthState.nome_perfil),
                rx.callout(
                    "O logout encerra a sessão apenas neste navegador; o token pode "
                    "permanecer válido no servidor por até 24 horas.",
                    color_scheme="gray",
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
