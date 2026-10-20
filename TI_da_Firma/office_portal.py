"""Telas Reflex de gestão e tarefas departamentais."""
import reflex as rx

from .office_state import OfficeState as S


def field(label: str, name: str, **props) -> rx.Component:
    return rx.vstack(rx.text(label, size="2", weight="medium"),
                     rx.input(name=name, width="100%", disabled=S.saving, **props),
                     align="start", spacing="1", width="100%")


def select(label: str, name: str, options, **props) -> rx.Component:
    return rx.vstack(rx.text(label, size="2", weight="medium"),
                     rx.select(options, name=name, required=True, placeholder=label,
                               disabled=S.saving, width="100%", **props),
                     align="start", spacing="1", width="100%")


def description() -> rx.Component:
    return rx.text_area(name="descricao", placeholder="Descrição", aria_label="Descrição",
                        width="100%", disabled=S.saving, min_height="6rem")


def form(kind: str, *children) -> rx.Component:
    return rx.form(
        rx.vstack(*children, rx.button("Salvar", type="submit", loading=S.saving),
                  width="100%", align="start", spacing="4"),
        on_submit=lambda data: S.submit(kind, data), reset_on_submit=False,
        key=S.form_revision.to_string(), width="100%",
    )


def user_form() -> rx.Component:
    return rx.vstack(
        rx.heading("Cadastrar usuário", size="5"),
        form("usuario", field("Nome", "name", required=True),
             field("E-mail", "email", type="email", required=True),
             field("Senha inicial", "password", type="password", id="office_password",
                   min_length=8, required=True, auto_complete=False),
             select("Perfil", "perfil", S.profile_labels, value=S.selected_profile,
                    on_change=S.select_profile),
             rx.cond(S.creating_technician,
                     rx.callout("Técnicos são vinculados obrigatoriamente à T.I.", width="100%"),
                     select("Departamento", "departamento", S.department_labels)),
             rx.text("A senha deve conter ao menos 8 caracteres, uma letra e um número.", size="2", color="gray")),
        width="100%", spacing="4", align="start")


def _owner_checkbox(row: rx.Var[dict[str, str]]) -> rx.Component:
    return rx.checkbox(
        row["label"], checked=S.selected_owners.contains(row["label"]),
        on_change=lambda checked: S.toggle_owner(row["label"], checked), disabled=S.saving,
    )


def task_form() -> rx.Component:
    return rx.vstack(
        rx.heading("Nova tarefa", size="5"),
        rx.text(rx.cond(S.ti_manager, "Selecione um ou mais técnicos de T.I.",
                        "Selecione um ou mais funcionários do seu departamento."), color="gray"),
        rx.cond(S.owner_options.length() == 0,
                rx.callout("Não há responsáveis elegíveis. Cadastre um usuário e atualize esta seção.", color_scheme="gray"),
                form("tarefa", field("Título", "titulo", required=True), description(),
                     rx.vstack(rx.text("Responsáveis", weight="medium"),
                               rx.foreach(S.owner_options, _owner_checkbox),
                               align="start", spacing="2", width="100%"),
                     rx.callout("Qualquer responsável pode concluir a tarefa inteira, informando a solução.", color_scheme="gray"),
                     select("Prioridade", "prioridade", S.priority_labels),
                     field("Prazo (opcional)", "prazo", type="date"),
                     field("Número do chamado (opcional)", "chamado_id", type="number", min=1))),
        align="start", spacing="4", width="100%")


def ticket_form() -> rx.Component:
    return rx.vstack(rx.heading("Abrir chamado", size="5"),
        form("chamado", field("Título", "titulo", required=True, max_length=200), description(),
             select("Categoria", "categoria", S.category_labels),
             select("Prioridade", "prioridade", S.priority_labels)),
        width="100%", align="start", spacing="4")


def ticket_card(row: rx.Var[dict[str, str]]) -> rx.Component:
    return rx.card(rx.vstack(rx.heading("#", row["id"], " · ", row["titulo"], size="4"),
        rx.badge(row["status_name"]), rx.text("Solicitante: ", row["requester_name"]),
        rx.text(row["category_name"], " · ", row["priority_name"], size="2"),
        rx.button("Visualizar", on_click=S.view_ticket(row["id"]), variant="soft"),
        align="start", spacing="2", width="100%"), width="100%")


def history_card(row: rx.Var[dict[str, str]]) -> rx.Component:
    return rx.card(rx.vstack(rx.text(row["author_name"], " · ", row["data"], size="2", weight="medium"),
        rx.text(row["mensagem"], white_space="pre-wrap"), align="start", width="100%"), width="100%")


def ticket_detail() -> rx.Component:
    return rx.vstack(rx.button("Voltar", on_click=S.navigate("chamados"), variant="soft"),
        rx.cond(S.ticket.contains("id"), rx.vstack(
            rx.heading("#", S.ticket["id"], " · ", S.ticket["titulo"], size="5"),
            rx.badge(S.ticket["status_name"]),
            rx.text("Solicitante: ", S.ticket["requester_name"], " (#", S.ticket["solicitante_id"], ")"),
            rx.text("Categoria: ", S.ticket["category_name"], " · Prioridade: ", S.ticket["priority_name"]),
            rx.text("Técnicos: ", S.ticket["technician_names"]),
            rx.text(S.ticket["descricao"], white_space="pre-wrap"),
            rx.cond(S.ticket["solucao_final"] != "", rx.text("Solução: ", S.ticket["solucao_final"], white_space="pre-wrap")),
            rx.heading("Histórico", size="4"),
            rx.cond(S.history_error != "", rx.callout(S.history_error, color_scheme="red"),
                    rx.cond(S.history.length() > 0, rx.foreach(S.history, history_card),
                            rx.text("Sem comentários.", color="gray"))),
            align="start", spacing="3", width="100%")),
        align="start", spacing="4", width="100%")


def task_card(row: rx.Var[dict[str, str]]) -> rx.Component:
    return rx.card(rx.vstack(rx.heading("#", row["id"], " · ", row["titulo"], size="4"),
        rx.badge(row["status_nome"]), rx.text("Prazo: ", row["prazo"], size="2"),
        rx.text("Responsáveis: ", row["member_names"], size="2"),
        rx.button("Ver tarefa", on_click=S.view_task(row["id"]), variant="soft"),
        align="start", spacing="2"), width="100%")


def task_detail() -> rx.Component:
    return rx.vstack(rx.button("Voltar às tarefas", on_click=S.navigate("tarefas"), disabled=S.saving),
        rx.cond(S.task.contains("id"), rx.vstack(
            rx.heading(S.task["titulo"], size="5"), rx.badge(S.task["status_nome"]),
            rx.text(S.task["descricao"], white_space="pre-wrap"),
            rx.text("Prazo: ", S.task["prazo"]),
            rx.text("Responsáveis: ", S.task["member_names"]),
            rx.cond(S.task["concluido_em"] != "",
                    rx.vstack(rx.text("Concluída em: ", S.task["concluido_em"]),
                              rx.text("Solução: ", S.task["solucao_aplicada"], white_space="pre-wrap"), align="start"),
                    rx.vstack(rx.text("Solução obrigatória", weight="medium"),
                              rx.text_area(value=S.solution, on_change=S.set_solution,
                                           aria_label="Solução da tarefa", min_height="8rem",
                                           disabled=S.saving, width="100%"),
                              rx.button("Concluir tarefa", on_click=S.submit("concluir", {}),
                                        loading=S.saving, disabled=S.solution.strip() == ""),
                              align="start", width="100%", spacing="3")),
            align="start", spacing="3", width="100%")),
        align="start", spacing="4", width="100%")


def office_portal(employee: bool = False) -> rx.Component:
    nav = (rx.flex(rx.button("Atualizar tarefas", on_click=S.navigate("tarefas"), disabled=S.saving | S.loading), gap="2") if employee else
           rx.flex(*[rx.button(label, on_click=S.navigate(section), variant="soft", disabled=S.saving)
                     for section, label in [("chamados", "Chamados"), ("novo_chamado", "Abrir chamado"),
                                             ("usuarios", "Cadastrar usuário"), ("nova_tarefa", "Nova tarefa")]],
                   wrap="wrap", gap="2"))
    return rx.vstack(nav,
        rx.cond(S.error != "", rx.callout(S.error, color_scheme="red", width="100%")),
        rx.cond(S.success != "", rx.callout(S.success, color_scheme="green", width="100%")),
        rx.cond(S.loading, rx.spinner(),
                rx.match(S.section,
                         ("chamados", rx.vstack(rx.heading("Chamados", size="5"),
                             rx.button("Atualizar", on_click=S.navigate("chamados"), variant="ghost"),
                             rx.cond(S.error == "", rx.cond(S.tickets.length() > 0,
                                 rx.foreach(S.tickets, ticket_card), rx.text("Nenhum chamado disponível."))), width="100%")),
                         ("novo_chamado", rx.cond(S.error == "", ticket_form())),
                         ("usuarios", rx.cond(S.profile_options.length() > 0, user_form())),
                         ("nova_tarefa", rx.cond(S.priority_options.length() > 0, task_form())),
                         ("detalhe", ticket_detail()),
                         ("tarefas", rx.vstack(rx.heading("Minhas tarefas", size="5"),
                             rx.cond(S.error == "", rx.cond(S.tasks.length() > 0, rx.foreach(S.tasks, task_card),
                                     rx.text("Você não tem tarefas atribuídas."))), width="100%")),
                         ("tarefa", task_detail()), rx.fragment())),
        width="100%", align="start", spacing="4", style={"overflow_wrap": "anywhere"})
