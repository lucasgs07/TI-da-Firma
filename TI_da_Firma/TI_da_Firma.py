"""Aplicação de gestão interna: login, home protegida e logout."""

import reflex as rx

from .auth_state import AuthState
from .ticket_state import TicketState


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
                    rx.link(
                        rx.button("Ver chamados", variant="soft"),
                        href="/chamados",
                    ),
                    rx.cond(
                        AuthState.pode_criar_chamado,
                        rx.link(
                            rx.button("Abrir chamado"),
                            href="/chamados/novo",
                        ),
                    ),
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


def ticket_create_page() -> rx.Component:
    ticket_form = rx.form(
        rx.vstack(
            rx.input(
                name="titulo",
                placeholder="Ex.: Computador não inicia",
                required=True,
                max_length=200,
                width="100%",
            ),
            rx.text_area(
                name="descricao",
                placeholder="Descreva o problema e as informações relevantes",
                required=True,
                max_length=10000,
                min_height="9rem",
                width="100%",
            ),
            rx.select.root(
                rx.select.trigger(placeholder="Selecione uma categoria", width="100%"),
                rx.select.content(
                    rx.foreach(
                        TicketState.categorias,
                        lambda item: rx.select.item(item["nome"], value=item["id"]),
                    ),
                ),
                name="categoria_chamado_id",
                value=TicketState.categoria_chamado_id,
                on_change=TicketState.selecionar_categoria,
                width="100%",
            ),
            rx.select.root(
                rx.select.trigger(placeholder="Selecione uma prioridade", width="100%"),
                rx.select.content(
                    rx.foreach(
                        TicketState.prioridades,
                        lambda item: rx.select.item(item["nome"], value=item["id"]),
                    ),
                ),
                name="prioridade_id",
                value=TicketState.prioridade_id,
                on_change=TicketState.selecionar_prioridade,
                width="100%",
            ),
            rx.cond(
                TicketState.erro_chamado != "",
                rx.callout(TicketState.erro_chamado, color_scheme="red", width="100%"),
            ),
            rx.button(
                "Registrar chamado",
                type="submit",
                loading=TicketState.enviando_chamado,
                disabled=TicketState.enviando_chamado | ~TicketState.tem_opcoes_chamado,
            ),
            spacing="4",
            width="100%",
        ),
        on_submit=TicketState.criar_chamado,
        width="100%",
    )

    created_message = rx.vstack(
        rx.callout(
            rx.vstack(
                rx.text("Chamado registrado com sucesso."),
                rx.text("Número: ", TicketState.chamado_criado_id),
                rx.text("Solicitante: ", TicketState.chamado_criado_solicitante),
                rx.text("Status: ", TicketState.chamado_criado_status),
                align="start",
            ),
            color_scheme="green",
            width="100%",
        ),
        rx.link(rx.button("Voltar ao início", variant="soft"), href="/"),
        spacing="4",
        width="100%",
    )

    form_content = rx.cond(
        TicketState.chamado_criado_id != "",
        created_message,
        rx.cond(
            TicketState.carregando_opcoes,
            rx.center(rx.spinner(), min_height="12rem"),
            rx.cond(
                TicketState.tem_opcoes_chamado,
                ticket_form,
                rx.vstack(
                    rx.callout(
                        rx.cond(
                            TicketState.erro_chamado != "",
                            TicketState.erro_chamado,
                            "Não há categorias e prioridades disponíveis para abrir chamados.",
                        ),
                        color_scheme="orange",
                        width="100%",
                    ),
                    rx.button(
                        "Tentar carregar novamente",
                        on_click=TicketState.carregar_opcoes_chamado,
                        variant="soft",
                    ),
                    spacing="3",
                    width="100%",
                ),
            ),
        ),
    )

    return rx.container(
        rx.cond(
            TicketState.autenticado,
            rx.cond(
                TicketState.pode_criar_chamado,
                rx.vstack(
                    rx.link("Voltar", href="/"),
                    rx.heading("Abrir chamado", size="7"),
                    rx.text("Solicitante: ", TicketState.perfil["name"]),
                    rx.cond(
                        TicketState.erro_chamado != "",
                        rx.callout(
                            TicketState.erro_chamado,
                            color_scheme="red",
                            width="100%",
                        ),
                    ),
                    form_content,
                    spacing="4",
                    align="start",
                    width="100%",
                    max_width="40rem",
                    padding_y="2rem",
                ),
                rx.callout(
                    "Seu perfil não tem permissão para abrir chamados.",
                    color_scheme="red",
                ),
            ),
            rx.cond(
                TicketState.erro_rede,
                rx.center(
                    rx.vstack(
                        rx.callout(
                            TicketState.erro_chamado,
                            color_scheme="red",
                            width="100%",
                        ),
                        rx.button(
                            "Tentar novamente",
                            on_click=TicketState.carregar_opcoes_chamado,
                        ),
                        align="center",
                        spacing="3",
                        width="100%",
                        max_width="32rem",
                    ),
                    min_height="80vh",
                ),
                rx.center(rx.spinner(), min_height="80vh"),
            ),
        ),
        width="100%",
    )


def tickets_page() -> rx.Component:
    ticket_list = rx.cond(
        TicketState.carregando_chamados,
        rx.center(rx.spinner(), min_height="12rem"),
        rx.cond(
            TicketState.erro_lista_chamados != "",
            rx.vstack(
                rx.callout(TicketState.erro_lista_chamados, color_scheme="red"),
                rx.button("Tentar novamente", on_click=TicketState.carregar_chamados),
                spacing="3",
                width="100%",
            ),
            rx.cond(
                TicketState.chamados.length() > 0,
                rx.vstack(
                    rx.foreach(
                        TicketState.chamados,
                        lambda ticket: rx.card(
                            rx.vstack(
                                rx.heading(ticket["titulo"], size="4"),
                                rx.text("Status: ", ticket["status_nome"]),
                                rx.text("Categoria: ", ticket["category_name"]),
                                rx.text("Prioridade: ", ticket["priority_name"]),
                                rx.text("Solicitante: ", ticket["requester_name"]),
                                rx.button(
                                    "Ver detalhes",
                                    on_click=TicketState.selecionar_chamado(ticket["id"]),
                                ),
                                align="start",
                                spacing="2",
                                width="100%",
                            ),
                            width="100%",
                        ),
                    ),
                    spacing="3",
                    width="100%",
                ),
                rx.text("Não há chamados disponíveis para sua conta."),
            ),
        ),
    )

    ticket_details = rx.vstack(
        rx.button(
            "Voltar à lista",
            on_click=TicketState.voltar_para_lista_chamados,
            variant="soft",
        ),
        rx.heading(TicketState.chamado_selecionado["titulo"], size="6"),
        rx.text("Status: ", TicketState.chamado_selecionado["status_nome"]),
        rx.text("Categoria: ", TicketState.chamado_selecionado["category_name"]),
        rx.text("Prioridade: ", TicketState.chamado_selecionado["priority_name"]),
        rx.text("Solicitante: ", TicketState.chamado_selecionado["requester_name"]),
        rx.text("Responsável: ", TicketState.chamado_selecionado["responsible_name"]),
        rx.text(TicketState.chamado_selecionado["descricao"]),
        rx.cond(
            TicketState.chamado_selecionado["solucao_final"] != "",
            rx.callout(
                rx.text("Solução final: ", TicketState.chamado_selecionado["solucao_final"]),
                color_scheme="green",
                width="100%",
            ),
        ),
        rx.cond(
            TicketState.erro_operacao_chamado != "",
            rx.callout(TicketState.erro_operacao_chamado, color_scheme="red", width="100%"),
        ),
        rx.cond(
            TicketState.pode_assumir_chamado_selecionado,
            rx.button(
                "Assumir chamado",
                on_click=TicketState.assumir_chamado_selecionado,
                loading=TicketState.operacao_chamado_em_andamento,
            ),
        ),
        rx.cond(
            TicketState.pode_atualizar_chamado_selecionado,
            rx.form(
                rx.vstack(
                    rx.heading("Atualizar atendimento", size="4"),
                    rx.select.root(
                        rx.select.trigger(placeholder="Selecione o status", width="100%"),
                        rx.select.content(
                            rx.foreach(
                                TicketState.status_operacionais,
                                lambda status: rx.select.item(status, value=status),
                            ),
                        ),
                        name="status_nome",
                        value=TicketState.status_atualizacao,
                        on_change=TicketState.selecionar_status_atualizacao,
                        width="100%",
                    ),
                    rx.text_area(
                        name="solucao_final",
                        placeholder="Solução final (obrigatória para resolver ou fechar)",
                        max_length=5000,
                        width="100%",
                    ),
                    rx.button(
                        "Salvar atualização",
                        type="submit",
                        loading=TicketState.operacao_chamado_em_andamento,
                    ),
                    spacing="3",
                    width="100%",
                ),
                on_submit=TicketState.atualizar_chamado,
                width="100%",
            ),
        ),
        rx.heading("Histórico de interações", size="4"),
        rx.cond(
            TicketState.interacoes_do_chamado.length() > 0,
            rx.vstack(
                rx.foreach(
                    TicketState.interacoes_do_chamado,
                    lambda interaction: rx.card(
                        rx.vstack(
                            rx.text(interaction["mensagem"]),
                            rx.text("Usuário #", interaction["user_id"], " · ", interaction["created_at"], size="1"),
                            align="start",
                            spacing="1",
                        ),
                        width="100%",
                    ),
                ),
                spacing="2",
                width="100%",
            ),
            rx.text("Ainda não há interações neste chamado."),
        ),
        rx.cond(
            TicketState.pode_responder_chamado_selecionado,
            rx.form(
                rx.vstack(
                    rx.text_area(
                        name="mensagem",
                        placeholder="Registrar uma interação",
                        required=True,
                        min_length=1,
                        width="100%",
                    ),
                    rx.button(
                        "Enviar interação",
                        type="submit",
                        loading=TicketState.operacao_chamado_em_andamento,
                    ),
                    spacing="3",
                    width="100%",
                ),
                on_submit=TicketState.registrar_interacao,
                width="100%",
            ),
        ),
        align="start",
        spacing="4",
        width="100%",
    )

    return rx.container(
        rx.cond(
            TicketState.autenticado,
            rx.vstack(
                rx.hstack(
                    rx.heading("Chamados", size="7"),
                    rx.spacer(),
                    rx.cond(
                        AuthState.pode_criar_chamado,
                        rx.link(rx.button("Abrir chamado"), href="/chamados/novo"),
                    ),
                    width="100%",
                ),
                rx.cond(
                    TicketState.chamado_selecionado_id != "",
                    ticket_details,
                    ticket_list,
                ),
                spacing="4",
                align="start",
                width="100%",
                max_width="48rem",
                padding_y="2rem",
            ),
            rx.center(rx.spinner(), min_height="80vh"),
        ),
        width="100%",
    )


app = rx.App()
app.add_page(home_page, route="/", on_load=AuthState.verificar_sessao)
app.add_page(login_page, route="/login", on_load=AuthState.verificar_login)
app.add_page(
    ticket_create_page,
    route="/chamados/novo",
    on_load=TicketState.carregar_opcoes_chamado,
)
app.add_page(
    tickets_page,
    route="/chamados",
    on_load=[AuthState.verificar_sessao, TicketState.carregar_chamados],
)
