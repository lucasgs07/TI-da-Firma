"""Navegação Nexo com os eventos e permissões dos portais existentes."""
import reflex as rx

from .auth_state import AuthState as A
from .office_state import OfficeState as O
from .admin_state import AdminState as D
from .design import BRAND


def _nav_button(label, event, active, disabled=False):
    return rx.button(label, on_click=event, variant="ghost", disabled=disabled,
                     class_name=rx.cond(active, "active", ""))


def navigation(tasks=False) -> rx.Component:
    return rx.box(
        rx.cond((A.perfil["perfil_id"] == "3") | (A.perfil["perfil_id"] == "4"),
            rx.fragment(
                rx.link(rx.cond(A.perfil["perfil_id"] == "3", "Todos os chamados", "Meus chamados"),
                        href="/", class_name="" if tasks else "active"),
                rx.link("Minhas tarefas", href="/tarefas", class_name="active" if tasks else ""))),
        rx.cond(A.perfil["perfil_id"] == "2", rx.fragment(*[
            _nav_button(label, O.navigate(section), O.section == section, O.saving | O.loading)
            for section, label in [("chamados", "Chamados"), ("novo_chamado", "Abrir chamado"),
                                   ("usuarios", "Cadastrar usuário"), ("nova_tarefa", "Nova tarefa")]])),
        rx.cond(A.perfil["perfil_id"] == "1", rx.fragment(*[
            _nav_button(label, D.navigate(section), D.section == section, D.saving | D.loading)
            for section, label in [("dashboard", "Dashboard"), ("chamados", "Chamados"),
                                   ("tarefas", "Tarefas"), ("usuarios", "Usuários"), ("logs", "Logs")]])),
        class_name="nexo-nav", aria_label="Navegação principal",
    )


def _profile():
    return rx.box(rx.text(A.perfil.get("name", ""), color="white"),
                  rx.text(A.nome_perfil, font_size="12px"),
                  rx.button("Sair da conta", on_click=A.sair, variant="ghost"), class_name="nexo-profile")


def workspace(content, tasks=False) -> rx.Component:
    label = rx.cond(A.perfil["perfil_id"] == "1",
        rx.match(D.section, ("dashboard", "Dashboard"), ("chamados", "Chamados"),
                 ("tarefas", "Tarefas"), ("usuarios", "Usuários"), ("logs", "Logs"), "Detalhes"),
        rx.cond(A.perfil["perfil_id"] == "2",
            rx.match(O.section, ("chamados", "Chamados"), ("novo_chamado", "Abrir chamado"),
                     ("usuarios", "Cadastrar usuário"), ("nova_tarefa", "Nova tarefa"), "Detalhes"),
            "Minhas tarefas" if tasks else rx.cond(A.perfil["perfil_id"] == "3", "Todos os chamados", "Meus chamados")))
    return rx.box(
        rx.box(rx.box(rx.text("Nexo"), rx.text("GESTÃO INTERNA"), class_name="nexo-brand"),
               rx.text("ÁREA DO ", A.nome_perfil.upper(), font_size="12px"),
               navigation(tasks), _profile(), class_name="nexo-sidebar"),
        rx.box(
            rx.box(rx.text("Nexo", font_size="18px", weight="bold"),
                rx.popover.root(rx.popover.trigger(rx.button("Menu", variant="ghost")),
                    rx.popover.content(navigation(tasks), _profile(), background="#142d29", width="260px")),
                class_name="nexo-mobile-header"),
            rx.box(rx.text("Workspace / ", label), rx.spacer(), rx.text("Ambiente interno"),
                   rx.text(A.nome_perfil, color=BRAND), class_name="nexo-topbar"),
            rx.box(content, class_name="nexo-main"), class_name="nexo-workspace"),
        class_name="nexo-shell",
    )
