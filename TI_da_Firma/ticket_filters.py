"""Filtros de consulta compartilhados; o escopo continua sendo aplicado pelo Xano."""
import reflex as rx

from . import xano_client as api
from .auth_state import AuthState, _ticket_view, _technical_ticket_view
from .office_state import OfficeState, ERRORS, option_rows, option_id
from .admin_state import AdminState


class TicketFilters(rx.State):
    priorities: list[dict[str, str]] = []
    statuses: list[dict[str, str]] = []
    priority: str = "Todas as prioridades"
    status: str = "Todos os status"
    requester: str = ""
    query: str = ""
    loading: bool = False
    error: str = ""

    @rx.var
    def priority_labels(self) -> list[str]:
        return ["Todas as prioridades"] + [r["label"] for r in self.priorities]

    @rx.var
    def status_labels(self) -> list[str]:
        return ["Todos os status"] + [r["label"] for r in self.statuses]

    @rx.event
    def set_priority(self, value: str):
        if not self.loading:
            self.priority = value

    @rx.event
    def set_status(self, value: str):
        if not self.loading:
            self.status = value

    @rx.event
    def set_requester(self, value: str):
        if not self.loading:
            self.requester = value

    @rx.event
    def set_query(self, value: str):
        if not self.loading:
            self.query = value

    @rx.event
    async def initialize(self):
        self.reset()
        auth = await self.get_state(AuthState)
        if not auth.autenticado:
            return
        try:
            self.priorities = option_rows(api.list_priorities(auth.auth_token))
            self.statuses = option_rows(api.ticket_statuses(auth.auth_token))
        except ERRORS as exc:
            if isinstance(exc, api.XanoRejected):
                auth._invalidar_sessao_rejeitada()
                yield rx.redirect("/login")
            else:
                self.error = "Não foi possível carregar as opções de filtros. Tente novamente."

    @rx.event
    async def apply(self, clear: bool = False):
        auth = await self.get_state(AuthState)
        office = await self.get_state(OfficeState)
        admin = await self.get_state(AdminState)
        if (self.loading or not auth.autenticado or office.loading or office.saving
                or admin.loading or admin.saving or auth.enviando_atendimento
                or auth.enviando_chamado or auth.carregando_tecnico or auth.carregando_chamados):
            return
        if clear:
            self.priority, self.status, self.requester, self.query = "Todas as prioridades", "Todos os status", "", ""
        self.error = ""
        try:
            role = auth._perfil_id()
            if role not in (1, 2, 3, 4):
                raise ValueError("Perfil não autorizado.")
            priority = None if self.priority == "Todas as prioridades" else option_id(self.priorities, self.priority)
            status = None if self.status == "Todos os status" else option_id(self.statuses, self.status)
            self.loading = True
            yield
            rows = api.search_tickets(auth.auth_token, priority, status, self.requester)
            query = self.query.strip().lstrip("#").casefold()
            rows = [r for r in rows if not query or query in str(r.get("id", ""))
                    or query in str(r.get("titulo", "")).casefold()]
            if role == 4:
                # Extra guard against a backend returning other employees' records.
                if any(str(r.get("solicitante_id")) != auth.perfil.get("id") for r in rows):
                    raise api.XanoUnavailable("Escopo de chamados inválido.")
                auth.chamados = [_ticket_view(r) for r in rows]
                auth.erro_chamados = ""
            elif role == 3:
                auth.chamados_tecnicos = [_technical_ticket_view(r) for r in rows]
                auth.erro_tecnico = ""
            elif role == 2:
                office.tickets = [_technical_ticket_view(r) for r in rows]
                office.error = ""
            else:
                admin.tickets = [_technical_ticket_view(r) for r in rows]
                admin.error = ""
            auth.busca_chamados, auth.filtro_status, auth.filtro_prioridade = "", "Todos os status", "Todas as prioridades"
        except ERRORS as exc:
            auth.chamados = auth.chamados_tecnicos = []
            office.tickets = admin.tickets = []
            if isinstance(exc, api.XanoRejected):
                auth._invalidar_sessao_rejeitada()
                self.reset()
                yield rx.redirect("/login")
            else:
                self.error = str(exc) if isinstance(exc, (ValueError, api.XanoOperationError, api.XanoConfigError)) else "Não foi possível aplicar os filtros. Tente novamente."
        finally:
            self.loading = False


def reset_visible_filters(root):
    filters = root.substates.get(TicketFilters.get_name())
    if filters is not None and not filters.loading:
        filters.priority, filters.status = "Todas as prioridades", "Todos os status"
        filters.requester = filters.query = filters.error = ""


def ticket_filters() -> rx.Component:
    from . import design as ui

    def control(label, component):
        return rx.vstack(
            rx.text(label, font_size="12px", font_weight="400", color=ui.INK),
            component, spacing="0", gap="8px", align="stretch", width="100%", min_width="0")

    return rx.box(rx.vstack(
        rx.flex(rx.heading("Pesquisar chamados", font_size="14px", font_weight="600", line_height="20px", margin="0"),
            rx.text("Combine os filtros para refinar a consulta.", color=ui.MUTED, font_size="10px", line_height="16px", margin="0"),
            gap="12px", align="center", wrap="wrap", width="100%"),
        rx.box(
            control("Número ou título", rx.input(placeholder="Ex.: #1048 ou impressora",
                aria_label="Número ou título do chamado", value=TicketFilters.query,
                on_change=TicketFilters.set_query, disabled=TicketFilters.loading, width="100%", height="38px", font_size="12px", border_radius="6px")),
            control("Prioridade", rx.select(TicketFilters.priority_labels, value=TicketFilters.priority,
                on_change=TicketFilters.set_priority, aria_label="Prioridade",
                disabled=TicketFilters.loading, width="100%", height="38px", font_size="12px", border_radius="6px")),
            control("Status", rx.select(TicketFilters.status_labels, value=TicketFilters.status,
                on_change=TicketFilters.set_status, aria_label="Status",
                disabled=TicketFilters.loading, width="100%", height="38px", font_size="12px", border_radius="6px")),
            control("Solicitante", rx.input(placeholder="Nome do solicitante", aria_label="Nome do solicitante",
                max_length=200, value=TicketFilters.requester, on_change=TicketFilters.set_requester,
                disabled=TicketFilters.loading, width="100%", height="38px", font_size="12px", border_radius="6px")),
            class_name="nexo-filter-fields", display="grid",
            grid_template_columns=rx.breakpoints(initial="minmax(0,1fr)", sm="minmax(0,1.57fr) minmax(0,1fr) minmax(0,1fr) minmax(0,1.34fr)"), gap="12px", width="100%"),
        rx.flex(
            rx.button("Aplicar filtros", on_click=TicketFilters.apply(False), loading=TicketFilters.loading,
                width="130px", height="34px", min_height="34px", font_size="12px", font_weight="400",
                background=ui.BRAND, color="white", border_radius="6px"),
            rx.button("Limpar", on_click=TicketFilters.apply(True), variant="outline", disabled=TicketFilters.loading,
                width="84px", height="34px", min_height="34px", font_size="12px", font_weight="400",
                color=ui.INK, background="white", border="1px solid " + ui.BORDER, box_shadow="none", border_radius="6px"),
            gap="10px", wrap="wrap"),
        rx.cond(TicketFilters.error != "", rx.callout(TicketFilters.error, color_scheme="red", width="100%")),
        width="100%", spacing="0", gap="16px", align="start"), width="100%",
        background="white", border="1px solid " + ui.BORDER, border_radius="10px", padding="20px",
        class_name="nexo-search-panel")


def ticket_results(rows, scope):
    from . import design as ui
    return rx.flex(rx.text(rows.length(), " chamados encontrados", font_size="14px"),
        rx.text(scope, color=ui.MUTED, font_size="12px"), gap="6", wrap="wrap", width="100%")
