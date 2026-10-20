"""Portal administrativo: indicadores, consultas, usuários e histórico."""
import reflex as rx

from .admin_state import AdminState as S


def record_card(row: rx.Var[dict[str, str]], kind: str) -> rx.Component:
    return rx.card(rx.vstack(
        rx.heading("#", row["id"], " · ", row["titulo"], size="4"),
        rx.cond(kind == "chamado", rx.text(row.get("status_name", "")), rx.text(row.get("status_nome", ""))),
        rx.button("Visualizar", on_click=S.view_record(kind, row["id"]), variant="soft"),
        align="start", spacing="2"), width="100%")


def detail(kind: str) -> rx.Component:
    row = S.ticket if kind == "chamado" else S.task
    return rx.vstack(
        rx.button("Voltar", on_click=S.navigate("chamados" if kind == "chamado" else "tarefas"), variant="soft"),
        rx.cond(row.contains("id"), rx.vstack(
            rx.heading("#", row["id"], " · ", row["titulo"], size="5"),
            rx.text("Solicitante: ", row.get("requester_name", ""), " (#", row["solicitante_id"], ")"),
            rx.text("Status: ", row.get("status_name", "") if kind == "chamado" else row["status_nome"]),
            rx.text("Responsáveis: ", row["technician_names"] if kind == "chamado" else row["member_names"]),
            rx.text(row["descricao"], white_space="pre-wrap"),
            rx.text("Solução: ", row["solucao_final"] if kind == "chamado" else row["solucao_aplicada"], white_space="pre-wrap"),
            rx.text("Conclusão: ", row["resolvido_em"] if kind == "chamado" else row["concluido_em"]),
            align="start", spacing="3", width="100%")),
        align="start", spacing="3", width="100%")


def user_form() -> rx.Component:
    return rx.form(rx.vstack(
        rx.input(name="name", placeholder="Nome", aria_label="Nome", required=True, disabled=S.saving, width="100%"),
        rx.input(name="email", placeholder="E-mail", aria_label="E-mail", type="email", required=True, disabled=S.saving, width="100%"),
        rx.input(name="password", id="admin_password", placeholder="Senha inicial", aria_label="Senha inicial", type="password",
                 required=True, min_length=8, disabled=S.saving, width="100%"),
        rx.text("Perfil"),
        rx.select(S.profile_labels, value=S.selected_profile, on_change=S.select_profile, disabled=S.saving, width="100%"),
        rx.cond(S.creating_technician, rx.callout("Técnicos são associados obrigatoriamente a T.I.", color_scheme="gray"),
                rx.select(S.department_labels, name="departamento", placeholder="Departamento", required=True,
                          disabled=S.saving, width="100%")),
        rx.button("Criar usuário", type="submit", loading=S.saving),
        align="start", spacing="3", width="100%"), on_submit=S.create_user, reset_on_submit=False,
        key=S.form_revision, width="100%")


def history_card(row: rx.Var[dict[str, str]]) -> rx.Component:
    return rx.card(rx.vstack(rx.text("Chamado #", row["chamado_id"], " · ", row["author_name"], " · ", row["data"], size="2"),
        rx.text(row["mensagem"], white_space="pre-wrap"), align="start", spacing="2"), width="100%")


def logs() -> rx.Component:
    return rx.vstack(
        rx.callout("Histórico de interações registradas nos chamados.", color_scheme="gray"),
        rx.form(rx.flex(
            rx.input(name="chamado_id", placeholder="Número do chamado (vazio = todos)", aria_label="Número do chamado",
                     type="number", min=1, disabled=S.saving),
            rx.button("Consultar", type="submit", disabled=S.saving), wrap="wrap", gap="2"),
            on_submit=S.filter_history, reset_on_submit=False),
        rx.text("Filtro aplicado: ", rx.cond(S.history_filter == "", "Todos os chamados", S.history_filter),
                " · Registros: ", S.history_total),
        rx.button("Baixar histórico CSV", on_click=S.export_history, loading=S.saving, disabled=S.error != ""),
        rx.cond(S.history.length() > 0, rx.foreach(S.history, history_card), rx.text("Sem interações registradas.")),
        rx.flex(rx.button("Anterior", on_click=S.history_page(S.page - 1), disabled=(S.page <= 1) | S.saving),
                rx.text("Página ", S.page),
                rx.button("Próxima", on_click=S.history_page(S.next_page), disabled=(S.next_page == 0) | S.saving), gap="3", wrap="wrap"),
        align="start", spacing="4", width="100%")


def dashboard() -> rx.Component:
    return rx.cond(S.metrics.contains("total"), rx.vstack(
        rx.flex(*[rx.card(rx.vstack(rx.text(label), rx.heading(S.metrics[key], size="7")), min_width="10rem")
                  for key, label in [("abertos", "Abertos"), ("em_andamento", "Em andamento"), ("finalizados", "Finalizados")]],
                wrap="wrap", gap="4", width="100%"),
        rx.text("Total: ", S.metrics["total"], " · Não classificados: ", S.metrics["nao_classificados"]),
        align="start", spacing="3", width="100%"))


def admin_portal() -> rx.Component:
    return rx.vstack(
        rx.heading("Administração", size="6"),
        rx.flex(*[rx.button(label, on_click=S.navigate(section), variant="soft", disabled=S.loading | S.saving)
                  for section, label in [("dashboard", "Dashboard"), ("chamados", "Chamados"), ("tarefas", "Tarefas"),
                                          ("usuarios", "Usuários"), ("logs", "Logs")]], wrap="wrap", gap="2"),
        rx.cond(S.error != "", rx.callout(S.error, color_scheme="red")),
        rx.cond(S.success != "", rx.callout(S.success, color_scheme="green")),
        rx.cond(S.loading, rx.spinner(), rx.match(S.section,
            ("dashboard", dashboard()),
            ("chamados", rx.vstack(rx.heading("Todos os chamados", size="5"),
                rx.cond(S.tickets.length() > 0, rx.foreach(S.tickets, lambda row: record_card(row, "chamado")), rx.text("Nenhum chamado.")), width="100%")),
            ("tarefas", rx.vstack(rx.heading("Todas as tarefas", size="5"),
                rx.cond(S.tasks.length() > 0, rx.foreach(S.tasks, lambda row: record_card(row, "tarefa")), rx.text("Nenhuma tarefa.")), width="100%")),
            ("detalhe_chamado", detail("chamado")), ("detalhe_tarefa", detail("tarefa")),
            ("usuarios", user_form()), ("logs", logs()), rx.fragment())),
        align="start", spacing="5", width="100%")
