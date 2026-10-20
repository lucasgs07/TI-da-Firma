"""Consultas administrativas e cadastro; sem eventos de atendimento."""
import csv
import io

import reflex as rx

from . import xano_client as api
from .auth_state import AuthState, _technical_ticket_view, _interaction_view
from .office_state import ERRORS, option_rows, option_id, public_task


CSV_FIELDS = ("id", "chamado_id", "created_at", "user_id", "author_name", "mensagem")


def history_csv(rows: list[dict]) -> bytes:
    def safe(value):
        text = "" if value is None else str(value)
        if text.lstrip().startswith(("=", "+", "-", "@")) or text.startswith(("\t", "\r", "\n")):
            return "'" + text
        return text
    output = io.StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(CSV_FIELDS)
    for row in rows:
        writer.writerow([safe(row.get(key)) for key in CSV_FIELDS])
    return output.getvalue().encode("utf-8-sig")


def history_view(row: dict) -> dict[str, str]:
    view = _interaction_view(row)
    view["chamado_id"] = str(row.get("chamado_id") or "")
    view["author_name"] = str(row.get("author_name") or "Autor indisponível")
    return view


class AdminState(rx.State):
    section: str = "dashboard"
    loading: bool = False
    saving: bool = False
    error: str = ""
    success: str = ""
    metrics: dict[str, int] = {}
    tickets: list[dict[str, str]] = []
    tasks: list[dict[str, str]] = []
    ticket: dict[str, str] = {}
    task: dict[str, str] = {}
    history: list[dict[str, str]] = []
    history_filter: str = ""
    _history_ticket_id: int | None = None
    _through_id: int | None = None
    page: int = 1
    next_page: int = 0
    history_total: int = 0
    department_options: list[dict[str, str]] = []
    profile_options: list[dict[str, str]] = []
    selected_profile: str = ""
    form_revision: int = 0

    @rx.var
    def department_labels(self) -> list[str]:
        return [r["label"] for r in self.department_options]

    @rx.var
    def profile_labels(self) -> list[str]:
        return [r["label"] for r in self.profile_options]

    @rx.var
    def creating_technician(self) -> bool:
        return any(r["id"] == "3" and r["label"] == self.selected_profile for r in self.profile_options)

    @rx.event
    def select_profile(self, value: str):
        if not self.saving and not self.loading:
            self.selected_profile = value

    async def _auth(self) -> AuthState:
        auth = await self.get_state(AuthState)
        if not auth.autenticado or auth._perfil_id() != 1:
            self.reset()
            raise api.XanoOperationError("Acesso administrativo não autorizado.")
        return auth

    async def _failure(self, exc: Exception):
        if isinstance(exc, api.XanoRejected):
            auth = await self.get_state(AuthState)
            auth._invalidar_sessao_rejeitada()
            self.reset()
            return rx.redirect("/login")
        self.error = (str(exc) if isinstance(exc, (ValueError, api.XanoOperationError, api.XanoConfigError))
                      else "Não foi possível carregar os dados. Tente novamente.")

    def _load_history(self, token: str):
        data = api.admin_history(token, self._history_ticket_id, self.page, self._through_id)
        self._through_id = data["through_id"]
        self.history = [history_view(r) for r in data["items"]]
        self.next_page = data.get("nextPage") or 0
        self.history_total = data.get("itemsTotal", 0)

    @rx.event
    async def initialize(self):
        self.reset()
        auth = await self.get_state(AuthState)
        if auth.autenticado and auth._perfil_id() == 1:
            async for event in self.navigate("dashboard"):
                yield event

    @rx.event
    async def navigate(self, section: str):
        if self.loading or self.saving:
            return
        self.error = self.success = ""
        self.ticket = self.task = self.metrics = {}
        self.history = self.tickets = self.tasks = []
        self.department_options = self.profile_options = []
        self.history_filter = ""
        self._history_ticket_id = self._through_id = None
        self.page, self.next_page, self.history_total = 1, 0, 0
        self.form_revision += 1
        try:
            auth = await self._auth()
            if section not in ("dashboard", "chamados", "tarefas", "usuarios", "logs"):
                raise ValueError("Seção inválida.")
            self.section, self.loading = section, True
            yield
            token = auth.auth_token
            if section == "dashboard":
                self.metrics = api.admin_metrics(token)
            elif section == "chamados":
                self.tickets = [_technical_ticket_view(r) for r in api.technician_tickets(token)]
            elif section == "tarefas":
                self.tasks = [public_task(r) for r in api.list_tasks(token)]
            elif section == "usuarios":
                self.department_options = option_rows(api.departments(token))
                self.profile_options = option_rows([r for r in api.profiles(token) if str(r["id"]) in ("1", "2", "3", "4")], "name")
                if not self.department_options or not self.profile_options:
                    raise ValueError("Perfis ou departamentos indisponíveis.")
                self.selected_profile = self.profile_options[0]["label"]
            else:
                self._load_history(token)
        except ERRORS as exc:
            yield await self._failure(exc)
        finally:
            self.loading = False

    @rx.event
    async def view_record(self, kind: str, record_id: str):
        if self.loading or self.saving:
            return
        self.ticket = self.task = {}
        self.history = []
        self.error = self.success = ""
        try:
            auth = await self._auth()
            if kind not in ("chamado", "tarefa") or int(record_id) < 1:
                raise ValueError("Registro inválido.")
            self.loading, self.section = True, "detalhe_" + kind
            yield
            if kind == "chamado":
                self.ticket = _technical_ticket_view(api.technician_ticket(int(record_id), auth.auth_token))
            else:
                self.task = public_task(api.get_task(auth.auth_token, int(record_id)))
        except ERRORS as exc:
            yield await self._failure(exc)
        finally:
            self.loading = False

    @rx.event
    async def filter_history(self, form: dict):
        if self.loading or self.saving:
            return
        self.error = self.success = ""
        self.history = []
        self.next_page = self.history_total = 0
        try:
            auth = await self._auth()
            value = str(form.get("chamado_id") or "").strip()
            ticket_id = int(value) if value else None
            if ticket_id is not None and ticket_id < 1:
                raise ValueError("Informe um número positivo de chamado.")
            self.history_filter = value
            self._history_ticket_id, self._through_id, self.page = ticket_id, None, 1
            self.loading = True
            yield
            self._load_history(auth.auth_token)
        except ERRORS as exc:
            yield await self._failure(exc)
        finally:
            self.loading = False

    @rx.event
    async def history_page(self, page: int):
        if self.loading or self.saving or self.section != "logs" or page < 1:
            return
        self.error = ""
        self.history = []
        try:
            auth = await self._auth()
            self.loading, self.page = True, page
            yield
            self._load_history(auth.auth_token)
        except ERRORS as exc:
            yield await self._failure(exc)
        finally:
            self.loading = False

    @rx.event
    async def export_history(self):
        if self.loading or self.saving or self.section != "logs":
            return
        self.error = self.success = ""
        try:
            auth = await self._auth()
            self.saving = True
            yield
            # Conteúdo só existe nesta chamada; nunca em estado sincronizado ou assets.
            rows = api.admin_history_all(auth.auth_token, self._history_ticket_id)
            data = history_csv(rows)
            await self._auth()
            yield rx.download(data=data, filename="historico-chamados.csv")
        except ERRORS as exc:
            yield await self._failure(exc)
        finally:
            self.saving = False

    @rx.event
    async def create_user(self, form: dict):
        if self.loading or self.saving:
            return
        self.error = self.success = ""
        try:
            auth = await self._auth()
            profile = option_id(self.profile_options, self.selected_profile)
            if profile not in (1, 2, 3, 4):
                raise ValueError("Perfil inválido.")
            department = 1 if profile == 3 else option_id(self.department_options, str(form.get("departamento") or ""))
            self.saving = True
            yield
            result = api.provision_user(auth.auth_token, str(form.get("name") or "").strip(),
                str(form.get("email") or "").strip(), str(form.get("password") or ""), profile, department)
            self.success = f"Usuário criado (#{result.get('id', '')})."
            self.form_revision += 1
        except ERRORS as exc:
            yield await self._failure(exc)
        finally:
            self.saving = False
        yield rx.set_value("admin_password", "")
