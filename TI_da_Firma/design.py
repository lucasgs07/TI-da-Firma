"""Componentes e tokens da identidade Nexo, traduzidos do Figma para Reflex."""
import reflex as rx

BRAND = "#16765b"
NAV = "#142d29"
INK = "#182c2a"
MUTED = "#647773"
BORDER = "#dfe7e4"
BG = "#f4f7f6"


def heading(title, subtitle="", action=None) -> rx.Component:
    return rx.flex(
        rx.vstack(rx.heading(title, font_size="28px", font_weight="600", line_height="1.45"),
                  rx.text(subtitle, color=MUTED, font_size="14px"), align="start", spacing="1", flex="1"),
        *([action] if action is not None else []),
        align="center", gap="4", wrap="wrap", width="100%", class_name="nexo-heading",
    )


def panel(*children, **props) -> rx.Component:
    return rx.box(*children, class_name="nexo-panel", **props)


def notice(text) -> rx.Component:
    return rx.box(rx.text(text, font_size="14px"), class_name="nexo-notice", width="100%")


def metric(label, value, caption) -> rx.Component:
    return panel(rx.vstack(rx.text(label, color=MUTED, font_size="12px"),
                           rx.text(value, font_size="32px", font_weight="600"),
                           rx.text(caption, color=MUTED, font_size="12px"),
                           align="start", spacing="2"), min_height="140px")


def badge(label) -> rx.Component:
    return rx.badge(label, variant="soft", class_name="nexo-badge",
                    color_scheme=rx.match(label,
                        ("Alta", "red"), ("Urgente", "red"),
                        ("Média", "amber"), ("Normal", "amber"),
                        ("Em atendimento", "amber"), ("Em análise", "amber"),
                        ("Aberto", "blue"), ("Pendente", "blue"), ("Inativo", "gray"), "green"))


def field(label, control) -> rx.Component:
    return rx.vstack(rx.text(label, font_size="14px", weight="medium"), control,
                     align="start", spacing="2", width="100%")


def table(headers: list[str], rows, render_row) -> rx.Component:
    return rx.box(rx.table.root(
        rx.table.header(rx.table.row(*[rx.table.column_header_cell(h) for h in headers])),
        rx.table.body(rx.foreach(rows, render_row)), width="100%"), class_name="nexo-table")


def ticket_table(rows, on_view, last_key="category_name", last_label="Categoria", last_fallback="—") -> rx.Component:
    def row(item):
        return rx.table.row(
            rx.table.cell(rx.text("#", item["id"], color=MUTED)),
            rx.table.cell(rx.button(item["titulo"], on_click=on_view(item["id"]),
                                    variant="ghost", class_name="nexo-record-link")),
            rx.table.cell(badge(item["status_name"])),
            rx.table.cell(badge(item["priority_name"])),
            rx.table.cell(item.get(last_key, last_fallback)),
        )

    def card(item):
        return panel(rx.vstack(
            rx.text("#", item["id"], font_size="12px", color=MUTED),
            rx.button(item["titulo"], on_click=on_view(item["id"]), variant="ghost",
                      class_name="nexo-record-link", font_size="18px", font_weight="600"),
            badge(item["status_name"]), align="start", spacing="5"))

    return rx.fragment(
        rx.box(table(["Nº", "Solicitação", "Status", "Prioridade", last_label], rows, row),
               class_name="nexo-desktop-records", width="100%"),
        rx.box(rx.vstack(rx.foreach(rows, card), spacing="4", width="100%"),
               class_name="nexo-mobile-records", width="100%"),
    )


def empty(title, text, action=None) -> rx.Component:
    return panel(rx.vstack(rx.heading(title, size="4"), rx.text(text, color=MUTED),
                           *([action] if action is not None else []), align="start", spacing="4"), width="100%")


APP_STYLE = {
    "font_family": "Inter, sans-serif", "font_size": "14px", "line_height": "1.45",
    "color": INK, "background": BG,
    rx.button: {"cursor": "pointer", "min_height": "44px", "border_radius": "8px", "font_weight": "500"},
    rx.input: {"height": "48px", "border_radius": "8px"},
    rx.text_area: {"min_height": "112px", "border_radius": "8px"},
    rx.card: {"background": "white", "border": f"1px solid {BORDER}", "box_shadow": "none", "border_radius": "12px", "padding": "24px"},
}
