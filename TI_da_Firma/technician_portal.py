"""Componentes Reflex da área de atendimento técnico."""
import reflex as rx

from .auth_state import AuthState
from .xano_client import OPERATIONAL_STATUSES


def _ticket(ticket: rx.Var[dict[str, str]]) -> rx.Component:
    return rx.card(
        rx.flex(
            rx.vstack(
                rx.text("#", ticket["id"], " · ", ticket["titulo"], weight="bold", size="4"),
                rx.badge(ticket["status_name"], variant="soft"),
                rx.text("Solicitante: ", ticket["requester_name"], " (#", ticket["solicitante_id"], ")", size="2"),
                rx.text(ticket["category_name"], " · Prioridade: ", ticket["priority_name"], size="2", color="gray"),
                rx.text("Técnicos: ", ticket["technician_names"], size="2"),
                align="start", spacing="2", min_width="0", flex="1",
            ),
            rx.button("Visualizar chamado", on_click=AuthState.abrir_atendimento(ticket["id"]), variant="soft"),
            direction=rx.breakpoints(initial="column", sm="row"), gap="4", width="100%",
            align="start",
        ),
        width="100%", style={"overflow_wrap": "anywhere"},
    )


def _list() -> rx.Component:
    return rx.vstack(
        rx.flex(
            rx.vstack(
                rx.heading("Todos os chamados", size="6"),
                rx.text("Acompanhe as solicitações e participe do atendimento.", color="gray", size="2"),
                align="start", spacing="1", flex="1",
            ),
            rx.button("Atualizar lista", on_click=AuthState.atualizar_lista_tecnica,
                      loading=AuthState.carregando_tecnico, variant="soft"),
            gap="3", wrap="wrap", width="100%",
        ),
        rx.cond(
            AuthState.carregando_tecnico,
            rx.center(rx.spinner(), padding="2rem", width="100%"),
            rx.cond(
                AuthState.erro_tecnico == "",
                rx.cond(
                    AuthState.chamados_tecnicos.length() > 0,
                    rx.vstack(rx.foreach(AuthState.chamados_tecnicos, _ticket), spacing="3", width="100%"),
                    rx.callout("Nenhum chamado cadastrado.", color_scheme="gray", width="100%"),
                ),
            ),
        ),
        width="100%", spacing="5",
    )


def _comment(row: rx.Var[dict[str, str]]) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.flex(rx.text(row["author_name"], weight="bold"), rx.text(row["data"], size="1", color="gray"),
                    gap="3", wrap="wrap", width="100%", justify="between"),
            rx.text(row["mensagem"], white_space="pre-wrap", width="100%"),
            align="start", spacing="2", width="100%",
        ),
        width="100%", style={"overflow_wrap": "anywhere"},
    )


def _history() -> rx.Component:
    return rx.vstack(
        rx.flex(
            rx.heading("Histórico e comentários", size="4"),
            rx.button("Atualizar histórico", variant="ghost", on_click=AuthState.atualizar_historico,
                      loading=AuthState.carregando_historico, disabled=AuthState.enviando_atendimento),
            gap="3", wrap="wrap", justify="between", width="100%",
        ),
        rx.cond(
            AuthState.carregando_historico,
            rx.spinner(),
            rx.cond(
                AuthState.erro_historico != "",
                rx.callout(AuthState.erro_historico, color_scheme="red", width="100%"),
                rx.cond(
                    AuthState.historico.length() > 0,
                    rx.vstack(rx.foreach(AuthState.historico, _comment), spacing="3", width="100%"),
                    rx.text("Ainda não há comentários neste chamado.", color="gray", size="2"),
                ),
            ),
        ),
        rx.cond(
            AuthState.tecnico_associado,
            rx.vstack(
                rx.text("Adicionar comentário", weight="medium", size="2"),
                rx.text_area(value=AuthState.comentario, on_change=AuthState.set_comentario,
                             placeholder="Registre uma interação do atendimento", aria_label="Comentário",
                             disabled=AuthState.enviando_atendimento, width="100%", min_height="7rem"),
                rx.button("Enviar comentário", on_click=AuthState.executar_atendimento("comentar"),
                          loading=AuthState.enviando_atendimento,
                          disabled=AuthState.comentario.strip() == ""),
                align="start", width="100%", spacing="3",
            ),
            rx.callout("Você pode consultar o histórico. Para comentar, é necessário estar associado ao chamado.",
                       color_scheme="gray", width="100%"),
        ),
        width="100%", spacing="4", align="start",
    )


def _context() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading("Informações do chamado", size="4"),
            rx.text("Solicitante", size="1", color="gray"),
            rx.text(AuthState.atendimento["requester_name"], " (#", AuthState.atendimento["solicitante_id"], ")"),
            rx.separator(),
            rx.text("Categoria: ", AuthState.atendimento["category_name"], size="2"),
            rx.text("Prioridade: ", AuthState.atendimento["priority_name"], size="2"),
            rx.text("Técnicos associados", size="2", weight="bold"),
            rx.text(AuthState.atendimento["technician_names"], size="2"),
            rx.cond(AuthState.tecnico_associado, rx.badge("Você está associado", color_scheme="green")),
            rx.cond(
                AuthState.pode_associar,
                rx.button("Associar a mim", on_click=AuthState.executar_atendimento("associar"),
                          loading=AuthState.enviando_atendimento, width="100%"),
            ),
            rx.separator(),
            rx.heading("Atendimento", size="4"),
            rx.cond(
                AuthState.pode_atualizar_atendimento,
                rx.vstack(
                    rx.text("Status", size="2", weight="medium"),
                    rx.select(OPERATIONAL_STATUSES, value=AuthState.status_destino,
                              on_change=AuthState.set_status_destino, aria_label="Status do atendimento",
                              disabled=AuthState.enviando_atendimento, width="100%"),
                    rx.text("Solução final", size="2", weight="medium"),
                    rx.text_area(value=AuthState.solucao, on_change=AuthState.set_solucao,
                                 placeholder="Obrigatória para resolver ou fechar", aria_label="Solução final",
                                 max_length=5000, disabled=AuthState.enviando_atendimento,
                                 min_height="8rem", width="100%"),
                    rx.button("Salvar atendimento", on_click=AuthState.executar_atendimento("status"),
                              loading=AuthState.enviando_atendimento, width="100%"),
                    align="start", width="100%", spacing="3",
                ),
                rx.text("Alterações de status exigem associação e um chamado ainda não concluído.", size="2", color="gray"),
            ),
            align="start", width="100%", spacing="3",
        ),
        width="100%", style={"overflow_wrap": "anywhere"},
    )


def _detail() -> rx.Component:
    return rx.vstack(
        rx.button("Voltar aos chamados", on_click=AuthState.voltar_lista_tecnica, variant="soft",
                  disabled=AuthState.enviando_atendimento),
        rx.cond(
            AuthState.carregando_tecnico,
            rx.spinner(),
            rx.cond(
                AuthState.atendimento.contains("id"),
                rx.vstack(
                    rx.heading("#", AuthState.atendimento["id"], " · ", AuthState.atendimento["titulo"], size="6"),
                    rx.badge(AuthState.atendimento["status_name"], size="2"),
                    rx.grid(
                        _context(),
                        rx.vstack(
                            rx.card(
                                rx.vstack(
                                    rx.heading("Descrição", size="4"),
                                    rx.text(AuthState.atendimento["descricao"], white_space="pre-wrap"),
                                    rx.cond(
                                        AuthState.atendimento["solucao_final"] != "",
                                        rx.vstack(rx.heading("Solução registrada", size="4"),
                                                  rx.text(AuthState.atendimento["solucao_final"], white_space="pre-wrap"),
                                                  align="start", width="100%"),
                                    ),
                                    align="start", spacing="3", width="100%",
                                ), width="100%",
                            ),
                            _history(), width="100%", min_width="0", spacing="5",
                        ),
                        grid_template_columns=rx.breakpoints(initial="minmax(0, 1fr)", sm="minmax(16rem, 1fr) minmax(0, 2fr)"),
                        gap="5", width="100%", align_items="start",
                    ),
                    align="start", spacing="4", width="100%", style={"overflow_wrap": "anywhere"},
                ),
            ),
        ),
        align="start", width="100%", spacing="4",
    )


def technician_portal() -> rx.Component:
    return rx.vstack(
        rx.cond(AuthState.erro_tecnico != "", rx.callout(AuthState.erro_tecnico, color_scheme="red", width="100%")),
        rx.cond(AuthState.sucesso_tecnico != "", rx.callout(AuthState.sucesso_tecnico, color_scheme="green", width="100%")),
        rx.cond(AuthState.tela_tecnico == "detalhe", _detail(), _list()),
        width="100%", spacing="4",
    )
