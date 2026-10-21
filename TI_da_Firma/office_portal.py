"""Telas Reflex de gestão e tarefas departamentais."""
import reflex as rx

from .office_state import OfficeState as S
from . import design as ui
from .ticket_filters import TicketFilters, ticket_filters, ticket_results


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
        ui.heading("Transforme uma demanda em ação.", rx.cond(S.ti_manager,
            "Atribua a tarefa a um ou mais técnicos de T.I.", "Atribua a tarefa a um ou mais funcionários do seu departamento.")),
        rx.box(ui.panel(
            rx.cond(S.owner_options.length() == 0,
                ui.empty("Sem responsáveis elegíveis", "Cadastre um usuário e atualize esta seção."),
                rx.form(rx.vstack(
                    field("Título *", "titulo", required=True),
                    ui.field("Descrição", description()),
                    rx.vstack(rx.text("Responsáveis *", weight="medium"),
                        rx.flex(rx.foreach(S.owner_options, _owner_checkbox), gap="4", wrap="wrap",
                                background=ui.BG, padding="12px", width="100%"), align="start", width="100%", spacing="3"),
                    rx.box(select("Prioridade *", "prioridade", S.priority_labels),
                           field("Prazo · opcional", "prazo", type="date"), class_name="nexo-pair"),
                    field("Nº do chamado · opcional", "chamado_id", type="number", min=1),
                    rx.button("Criar tarefa", type="submit", loading=S.saving),
                    align="start", spacing="5", width="100%"),
                    on_submit=lambda data: S.submit("tarefa", data), reset_on_submit=False,
                    key=S.form_revision.to_string(), width="100%"))),
            ui.panel(rx.vstack(rx.heading("Trabalho compartilhado", size="4"),
                rx.text("Qualquer responsável pode concluir a tarefa inteira, informando uma única solução.", color=ui.MUTED),
                ui.notice(rx.cond(S.ti_manager, "Você pode selecionar técnicos de T.I.",
                                  "Você pode selecionar funcionários do seu departamento.")), align="start", spacing="5")),
            class_name="nexo-form-columns"), width="100%", spacing="5")


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
    return rx.vstack(
        rx.button("Voltar às tarefas", on_click=S.navigate("tarefas"), disabled=S.saving, variant="outline"),
        rx.cond(S.task.contains("id"), rx.vstack(
            ui.heading(S.task["titulo"], rx.fragment("Minhas tarefas / #", S.task["id"], " · Prazo: ", S.task["prazo"])),
            rx.box(ui.panel(rx.vstack(
                rx.heading("O que precisa ser feito", size="4"),
                rx.text(S.task["descricao"], white_space="pre-wrap"),
                rx.cond(S.task["concluido_em"] != "",
                    rx.vstack(ui.badge(S.task["status_nome"]), rx.text("Concluída em: ", S.task["concluido_em"]),
                              rx.text("Solução: ", S.task["solucao_aplicada"], white_space="pre-wrap"), align="start"),
                    rx.vstack(
                        ui.field("Solução aplicada *", rx.text_area(value=S.solution, on_change=S.set_solution,
                            aria_label="Solução da tarefa", placeholder="Descreva o que foi feito para concluir a tarefa.",
                            disabled=S.saving, width="100%")),
                        ui.notice("Ao concluir, esta tarefa será finalizada para todos os responsáveis."),
                        rx.button("Concluir tarefa", on_click=S.submit("concluir", {}), loading=S.saving,
                                  disabled=S.solution.strip() == ""), align="start", width="100%", spacing="5")),
                align="start", spacing="5", width="100%")),
                ui.panel(rx.vstack(rx.text("Responsáveis", color=ui.MUTED, font_size="12px"),
                    rx.text(S.task["member_names"]), ui.badge(S.task["status_nome"]),
                    rx.text("Chamado vinculado", color=ui.MUTED, font_size="12px"),
                    rx.text(rx.cond(S.task["chamado_id"] != "", S.task["chamado_id"], "Sem vínculo")),
                    rx.text("Concluir a tarefa não altera o status do chamado.", color=ui.MUTED),
                    align="start", spacing="5")), class_name="nexo-form-columns"),
            align="start", spacing="5", width="100%")), align="start", spacing="5", width="100%")


def _tasks() -> rx.Component:
    def row(item):
        return rx.table.row(rx.table.cell("#", item["id"]),
            rx.table.cell(rx.button(item["titulo"], on_click=S.view_task(item["id"]), variant="ghost", class_name="nexo-record-link")),
            rx.table.cell(ui.badge(item["status_nome"])), rx.table.cell(item["prazo"]), rx.table.cell(item["member_names"]))
    return rx.vstack(
        ui.heading("Seu trabalho, organizado.", "Veja as tarefas atribuídas a você e registre a solução ao concluir.",
            rx.button("Atualizar tarefas", on_click=S.navigate("tarefas"), disabled=S.saving | S.loading, variant="outline")),
        rx.grid(ui.metric("Pendentes", S.task_summary["pending"], "Tarefas carregadas atribuídas a você"),
                ui.metric("Concluídas", S.task_summary["completed"], "Tarefas carregadas atribuídas a você"),
                columns=rx.breakpoints(initial="1", sm="2"), gap="16px", width="100%", max_width="516px"),
        rx.cond(S.error == "", rx.cond(S.tasks.length() > 0,
            ui.table(["Tarefa", "Atividade", "Status", "Prazo", "Responsáveis"], S.tasks, row),
            ui.empty("Nenhuma tarefa por aqui", "As tarefas atribuídas a você aparecerão nesta área."))),
        ui.notice("Qualquer responsável pode concluir a tarefa inteira. A solução fica registrada para todos."),
        align="start", spacing="5", width="100%")


def _manager_tickets() -> rx.Component:
    return rx.vstack(
        ui.heading("Chamados do departamento", rx.cond(S.ti_manager,
            "Consulte os chamados de toda a empresa.", "Chamados dos membros do seu departamento."),
            rx.button("+ Abrir chamado", on_click=S.navigate("novo_chamado"), disabled=S.saving | S.loading)),
        ui.notice(rx.cond(S.ti_manager, "Seu escopo é global. Os chamados são exibidos para consulta.",
                         "Seu escopo é o seu departamento. Os chamados são exibidos para consulta.")),
        ticket_filters(), ticket_results(S.tickets, rx.cond(S.ti_manager, "Consulta global", "Somente seu departamento")),
        rx.cond(S.error == "", rx.cond(S.tickets.length() > 0,
            ui.ticket_table(S.tickets, S.view_ticket, "requester_name", "Solicitante"),
            ui.empty("Nenhum chamado disponível", "Não há solicitações no seu escopo de consulta."))),
        ui.panel(rx.vstack(rx.heading("Próximos passos", size="4"),
            rx.text("Crie tarefas ou cadastre um novo integrante conforme as permissões do seu departamento.", color=ui.MUTED),
            rx.flex(rx.button("Nova tarefa", on_click=S.navigate("nova_tarefa"), disabled=S.saving | S.loading),
                    rx.button("Cadastrar usuário", on_click=S.navigate("usuarios"), variant="outline", disabled=S.saving | S.loading),
                    rx.button("Atualizar", on_click=TicketFilters.apply(False), variant="outline", disabled=S.saving | S.loading),
                    gap="3", wrap="wrap"), align="start", spacing="5"), width="100%"),
        width="100%", align="start", spacing="5")


def office_portal(employee: bool = False) -> rx.Component:
    return rx.vstack(
        rx.cond(S.error != "", rx.callout(S.error, color_scheme="red", width="100%")),
        rx.cond(S.success != "", rx.callout(S.success, color_scheme="green", width="100%")),
        rx.cond(S.loading, rx.spinner(), rx.match(S.section,
            ("chamados", _manager_tickets()),
            ("novo_chamado", rx.cond(S.error == "", ui.panel(ticket_form(), width="100%"))),
            ("usuarios", rx.cond(S.profile_options.length() > 0, ui.panel(user_form(), width="100%"))),
            ("nova_tarefa", rx.cond(S.priority_options.length() > 0, task_form())),
            ("detalhe", ticket_detail()), ("tarefas", _tasks()), ("tarefa", task_detail()), rx.fragment())),
        width="100%", align="start", spacing="5", style={"overflow_wrap": "anywhere"})
