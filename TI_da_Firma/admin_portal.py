"""Portal administrativo: indicadores, consultas, usuários e histórico."""
import reflex as rx

from .admin_state import AdminState as S
from . import design as ui
from .ticket_filters import ticket_filters, ticket_results


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
        ui.field("Nome *", rx.input(name="name", placeholder="Ana Souza", aria_label="Nome", required=True, disabled=S.saving, width="100%")),
        ui.field("E-mail *", rx.input(name="email", placeholder="ana.souza@empresa.com.br", aria_label="E-mail", type="email", required=True, disabled=S.saving, width="100%")),
        rx.box(
            ui.field("Perfil *", rx.select(S.profile_labels, value=S.selected_profile, on_change=S.select_profile, disabled=S.saving, width="100%")),
            ui.field("Departamento *", rx.cond(S.creating_technician,
                rx.input(value="T.I. · obrigatório para técnicos", disabled=True, width="100%"),
                rx.select(S.department_labels, name="departamento", placeholder="Departamento", required=True, disabled=S.saving, width="100%"))),
            class_name="nexo-pair"),
        ui.field("Senha inicial *", rx.input(name="password", id="admin_password", placeholder="••••••••••••", aria_label="Senha inicial", type="password",
                 required=True, min_length=8, auto_complete=False, disabled=S.saving, width="100%")),
        rx.text("Pelo menos 8 caracteres, uma letra e um número.", font_size="12px", color=ui.MUTED),
        rx.button("Cadastrar usuário", type="submit", loading=S.saving, width="200px"),
        align="start", gap="20px", width="100%"), on_submit=S.create_user, reset_on_submit=False,
        key=S.form_revision, width="100%")


def user_edit_form() -> rx.Component:
    return rx.form(rx.vstack(
        rx.heading("Dados pessoais", size="4"),
        rx.text("Mantenha as informações de identificação atualizadas.", color=ui.MUTED),
        ui.field("Nome completo *", rx.input(name="name", default_value=S.user.get("name", ""), required=True, disabled=S.saving, width="100%")),
        ui.field("E-mail *", rx.input(name="email", type="email", default_value=S.user.get("email", ""), required=True, disabled=S.saving, width="100%")),
        rx.separator(width="100%"),
        rx.heading("Acesso ao sistema", size="4"),
        rx.box(
            ui.field("Perfil *", rx.select(S.profile_labels, value=S.selected_profile, on_change=S.select_profile, disabled=S.saving, width="100%")),
            rx.cond(S.creating_technician, ui.notice("Técnicos pertencem obrigatoriamente a T.I."),
                ui.field("Departamento", rx.select(S.edit_department_labels, name="departamento", required=True,
                    default_value=S.edited_department_label, disabled=S.saving, width="100%"))),
            class_name="nexo-pair"),
        rx.box(ui.field("Status *", rx.select(["Ativo", "Inativo"], name="status",
            default_value=rx.cond(S.user.get("status", "") == "", "Ativo", S.user.get("status", "")),
            required=True, disabled=S.saving, width="100%")), width=rx.breakpoints(initial="100%", sm="49%")),
        rx.flex(rx.button("Salvar alterações", type="submit", loading=S.saving),
            rx.button("Cancelar", type="button", on_click=S.show_user_mode("list"), disabled=S.saving, variant="outline"),
            gap="3", wrap="wrap"),
        align="start", spacing="4", width="100%"), on_submit=S.save_user,
        reset_on_submit=False, key=S.form_revision, width="100%")


def user_summary() -> rx.Component:
    return ui.panel(rx.vstack(
        rx.avatar(fallback=S.user.get("name", "")[:2], size="4", radius="full"),
        rx.heading(S.user.get("name", ""), size="4"),
        rx.text(S.user.get("email", ""), color=ui.MUTED, overflow_wrap="anywhere"),
        ui.badge(S.user.get("status", "")),
        rx.text("PERFIL ATUAL", color=ui.MUTED, font_size="12px"),
        rx.text(S.selected_profile, " · ", S.edited_department_label),
        rx.box(rx.text("Confira antes de salvar", weight="medium"),
            rx.text("O perfil e o departamento definem as áreas e os dados que a pessoa pode acessar.",
                color=ui.MUTED, margin_top="8px"), class_name="nexo-summary-note"),
        align="start", spacing="4", width="100%"))


def users() -> rx.Component:
    def row(item):
        return rx.table.row(rx.table.cell(item["name"]), rx.table.cell(item["email"]),
            rx.table.cell(item["profile_name"]), rx.table.cell(item["department_name"]),
            rx.table.cell(rx.cond(item["status"] == "Inativo", rx.text("Inativo", color=ui.MUTED, font_size="12px"), ui.badge(item["status"]))),
            rx.table.cell(rx.button("Editar", on_click=S.open_user(item["id"]), variant="outline")))
    return rx.vstack(
        rx.cond(S.user_mode == "edit",
            ui.heading("Editar usuário", rx.fragment("Usuários / ", S.user.get("name", ""))),
            rx.cond(S.user_mode == "create", rx.fragment(),
                ui.heading("Usuários", "Consulte as pessoas cadastradas e gerencie seus dados de acesso.",
                    rx.button("+ Cadastrar usuário", on_click=S.show_user_mode("create"))))),
        rx.match(S.user_mode,
            ("create", rx.vstack(ui.user_registration(user_form()),
                rx.button("Voltar à lista", on_click=S.show_user_mode("list"), variant="outline", disabled=S.saving), width="100%", spacing="4")),
            ("edit", rx.box(ui.panel(user_edit_form()), user_summary(), class_name="nexo-user-columns")),
            rx.vstack(
                rx.flex(rx.heading("Diretório de usuários", size="4"), rx.text(S.users_total, " usuários", color=ui.MUTED, font_size="12px"), gap="16px", align="center"),
                rx.cond(S.users.length() > 0,
                    ui.table(["Nome", "E-mail", "Perfil", "Departamento", "Status", "Ações"], S.users, row),
                    rx.cond(S.error == "", ui.empty("Nenhum usuário", "Nenhum usuário encontrado nesta página."))),
                rx.flex(
                    rx.text("Exibindo ", S.users_first, "–", S.users_last, " de ", S.users_total,
                        " usuários · Página ", S.users_page, " de ", S.users_pages,
                        color=ui.MUTED, font_size="12px"),
                    rx.flex(
                        rx.button("Anterior", on_click=S.users_page_at(S.users_page - 1),
                            disabled=(S.users_page <= 1) | S.loading, variant="outline"),
                        rx.badge(S.users_page, variant="soft", class_name="nexo-page-current"),
                        rx.button("Próxima", on_click=S.users_page_at(S.users_next_page),
                            disabled=(S.users_next_page == 0) | S.loading, variant="outline"),
                        gap="3", align="center"),
                    justify="between", align="center", gap="4", wrap="wrap", width="100%"),
                rx.button("Atualizar lista", on_click=S.users_page_at(S.users_page), disabled=S.loading, variant="outline"),
                spacing="5", align="start", width="100%", class_name="nexo-user-directory")), width="100%", spacing="5")


def history_card(row: rx.Var[dict[str, str]]) -> rx.Component:
    return rx.card(rx.vstack(rx.text("Chamado #", row["chamado_id"], " · ", row["author_name"], " · ", row["data"], size="2"),
        rx.text(row["mensagem"], white_space="pre-wrap"), align="start", spacing="2"), width="100%")


def logs() -> rx.Component:
    def row(item):
        return rx.table.row(rx.table.cell(item["id"]), rx.table.cell("#", item["chamado_id"]),
            rx.table.cell(item["author_name"]), rx.table.cell(item["data"]),
            rx.table.cell(rx.text(item["mensagem"], white_space="pre-wrap")))
    return rx.vstack(
        ui.heading("O histórico, com contexto.", "Consulte interações registradas e exporte o histórico completo."),
        rx.form(rx.flex(
            rx.input(name="chamado_id", placeholder="Nº do chamado · opcional", aria_label="Número do chamado",
                     type="number", min=1, disabled=S.saving, width=rx.breakpoints(initial="100%", sm="360px"),
                     height="34px", font_size="12px", border_radius="6px"),
            rx.button("Aplicar filtro", type="submit", disabled=S.saving,
                      width="120px", height="34px", min_height="34px", font_size="12px", font_weight="400",
                      background=ui.BRAND, color="white", border_radius="6px"),
            rx.button("Baixar histórico CSV", type="button", on_click=S.export_history,
                      loading=S.saving, disabled=S.error != "", variant="outline",
                      width="176px", height="34px", min_height="34px", font_size="12px", font_weight="400",
                      background="white", color=ui.INK, border="1px solid " + ui.BORDER,
                      box_shadow="none", border_radius="6px"), gap="12px", align="center", wrap="wrap"),
            on_submit=S.filter_history, reset_on_submit=False, width="100%"),
        ui.notice(rx.fragment("Filtro aplicado: ", rx.cond(S.history_filter == "", "Todos os chamados", S.history_filter),
                              ". A exportação usa este filtro aplicado.")),
        rx.cond(S.error == "", rx.cond(S.history.length() > 0,
            ui.table(["ID", "Chamado", "Autor", "Data (UTC)", "Mensagem"], S.history, row),
            ui.empty("Sem interações registradas", "Nenhuma interação corresponde ao filtro aplicado."))),
        rx.flex(rx.button("Anterior", on_click=S.history_page(S.page - 1), disabled=(S.page <= 1) | S.saving, variant="outline"),
            rx.text("Página ", S.page, " · ", S.history_total, " interações", color=ui.MUTED, font_size="12px"),
            rx.button("Próxima", on_click=S.history_page(S.next_page), disabled=(S.next_page == 0) | S.saving, variant="outline"),
            gap="3", wrap="wrap", align="center"), align="start", spacing="5", width="100%")


def dashboard() -> rx.Component:
    groups = [("abertos", "Abertos", "Aguardando atendimento", "blue"),
              ("em_andamento", "Em andamento", "Análise e atendimento", "amber"),
              ("finalizados", "Finalizados", "Resolvidos ou fechados", "green"),
              ("nao_classificados", "Não classificados", "Revise a classificação", "gray")]
    return rx.vstack(
        ui.heading("Uma visão clara da operação.", "Acompanhe o panorama global dos chamados da empresa."),
        rx.cond(S.metrics.contains("total"), rx.vstack(
            rx.grid(*[ui.metric(label, S.metrics[key], caption) for key, label, caption, _ in groups],
                columns=rx.breakpoints(initial="1", sm="2", lg="4"), gap="16px", width="100%"),
            rx.box(ui.panel(rx.vstack(
                rx.heading("Onde estão os ", S.metrics["total"], " chamados", size="4"),
                rx.text("Distribuição por grupo de status", color=ui.MUTED, font_size="12px"),
                *[rx.flex(rx.text(label, width="160px", flex_shrink="0"),
                          rx.progress(value=S.metrics[key] * 100 / rx.cond(S.metrics["total"] > 0, S.metrics["total"], 1),
                                      max=100, color_scheme=color, height="10px", flex="1", aria_label=label),
                          rx.text(S.metrics[key], width="40px"), align="center", gap="4", width="100%")
                  for key, label, _, color in groups], align="start", spacing="6", width="100%")),
                ui.panel(rx.vstack(rx.text("TOTAL DE CHAMADOS", font_size="12px", color=ui.MUTED),
                    rx.text(S.metrics["total"], font_size="32px", font_weight="600"),
                    rx.text("Cada chamado é contado uma vez, mesmo com vários técnicos associados.", color=ui.MUTED),
                    rx.button("Consultar chamados", on_click=S.navigate("chamados"), variant="outline", width="100%"),
                    align="start", spacing="5")), class_name="nexo-form-columns"),
            ui.panel(rx.vstack(rx.heading("Acesso rápido", size="4"),
                rx.flex(*[
                    rx.button(label, on_click=S.navigate(target), variant="outline",
                        width="195px", max_width="100%", height="40px", min_height="40px",
                        background="white", color=ui.INK, border="1px solid " + ui.BORDER,
                        box_shadow="none", border_radius="8px", font_size="14px", font_weight="400")
                    for label, target in [("Cadastrar usuário", "usuarios"),
                                          ("Consultar tarefas", "tarefas"), ("Histórico e CSV", "logs")]
                ], gap="16px", wrap="wrap", width="100%"),
                align="start", spacing="5"), width="100%"),
            align="start", spacing="5", width="100%")), align="start", spacing="5", width="100%")


def admin_portal() -> rx.Component:
    return rx.vstack(
        rx.cond(S.error != "", rx.callout(S.error, color_scheme="red")),
        rx.cond(S.success != "", rx.callout(S.success, color_scheme="green")),
        rx.cond(S.loading, rx.spinner(), rx.match(S.section,
            ("dashboard", dashboard()),
            ("chamados", rx.vstack(ui.heading("Todos os chamados", "Consulta global das solicitações."), ticket_filters(), ticket_results(S.tickets, "Consulta global"),
                rx.cond(S.error == "", rx.cond(S.tickets.length() > 0,
                    ui.ticket_table(S.tickets, lambda value: S.view_record("chamado", value), "requester_name", "Solicitante"),
                    ui.empty("Nenhum chamado", "As solicitações registradas aparecerão aqui."))), width="100%", spacing="5")),
            ("tarefas", rx.vstack(ui.heading("Todas as tarefas", "Consulta das tarefas da empresa."),
                rx.cond(S.error == "", rx.cond(S.tasks.length() > 0,
                    rx.foreach(S.tasks, lambda row: record_card(row, "tarefa")), rx.text("Nenhuma tarefa."))), width="100%", spacing="5")),
            ("detalhe_chamado", detail("chamado")), ("detalhe_tarefa", detail("tarefa")),
            ("usuarios", users()),
            ("logs", logs()), rx.fragment())), align="start", spacing="5", width="100%")
