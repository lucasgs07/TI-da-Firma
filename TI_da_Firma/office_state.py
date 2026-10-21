"""Estado das operações gerenciais e das tarefas próprias do funcionário."""
import reflex as rx

from . import xano_client as api
from .auth_state import AuthState, _technical_ticket_view, _interaction_view

ERRORS = (api.XanoRejected, api.XanoOperationError, api.XanoUnavailable, api.XanoConfigError, ValueError)


def task_member_ids(row: dict) -> list[str]:
    """A lista nova prevalece; o responsável único só serve para tarefas legadas."""
    ids = row.get("responsaveis_ids")
    if isinstance(ids, list) and ids:
        return list(dict.fromkeys(str(member) for member in ids))
    legacy = row.get("responsavel_id")
    return [str(legacy)] if legacy else []


def public_task(row: dict) -> dict[str, str]:
    keys = ("id", "titulo", "descricao", "solucao_aplicada", "prazo", "concluido_em",
            "responsavel_id", "solicitante_id", "requester_name", "chamado_id", "prioridade_id", "status_nome")
    result = {k: str(row.get(k) or "") for k in keys}
    result["member_ids"] = ",".join(task_member_ids(row))
    result["member_names"] = ", ".join(
        str(member.get("name") or f"Usuário #{member.get('id')}")
        for member in row.get("responsaveis", []) if isinstance(member, dict)
    ) or ", ".join(f"Usuário #{member}" for member in task_member_ids(row))
    if not result["status_nome"]:
        result["status_nome"] = "Concluída" if row.get("concluido_em") else "Pendente"
    return result


def option_rows(rows: list[dict], name_key: str = "nome") -> list[dict[str, str]]:
    return [{"id": str(r["id"]), "label": f"{r.get(name_key) or r['id']} (#{r['id']})"} for r in rows]


def option_id(options: list[dict], label: str) -> int:
    for item in options:
        if item["label"] == label:
            return int(item["id"])
    raise ValueError("Selecione uma opção válida.")


class OfficeState(rx.State):
    section: str = "chamados"
    ti_manager: bool = False
    manager: bool = False
    loading: bool = False
    saving: bool = False
    error: str = ""
    success: str = ""
    history_error: str = ""
    tickets: list[dict[str, str]] = []
    ticket: dict[str, str] = {}
    history: list[dict[str, str]] = []
    tasks: list[dict[str, str]] = []
    task: dict[str, str] = {}
    department_options: list[dict[str, str]] = []
    profile_options: list[dict[str, str]] = []
    owner_options: list[dict[str, str]] = []
    selected_owners: list[str] = []
    category_options: list[dict[str, str]] = []
    priority_options: list[dict[str, str]] = []
    selected_profile: str = ""
    solution: str = ""
    form_revision: int = 0

    @rx.var
    def task_summary(self) -> dict[str, int]:
        completed = sum(bool(row.get("concluido_em")) for row in self.tasks)
        return {"pending": len(self.tasks) - completed, "completed": completed}

    @rx.var
    def department_labels(self) -> list[str]:
        return [r["label"] for r in self.department_options]

    @rx.var
    def profile_labels(self) -> list[str]:
        return [r["label"] for r in self.profile_options]

    @rx.var
    def owner_labels(self) -> list[str]:
        return [r["label"] for r in self.owner_options]

    @rx.var
    def category_labels(self) -> list[str]:
        return [r["label"] for r in self.category_options]

    @rx.var
    def priority_labels(self) -> list[str]:
        return [r["label"] for r in self.priority_options]

    @rx.var
    def creating_technician(self) -> bool:
        return any(r["id"] == "3" and r["label"] == self.selected_profile for r in self.profile_options)

    @rx.event
    def select_profile(self, value: str):
        if not self.saving:
            self.selected_profile = value

    @rx.event
    def set_solution(self, value: str):
        if not self.saving:
            self.solution = value

    @rx.event
    def toggle_owner(self, label: str, checked: bool):
        if self.saving or self.loading or label not in self.owner_labels:
            return
        if checked:
            self.selected_owners = list(dict.fromkeys([*self.selected_owners, label]))
        else:
            self.selected_owners = [item for item in self.selected_owners if item != label]

    async def _auth(self, roles=(2, 3, 4)) -> AuthState:
        auth = await self.get_state(AuthState)
        if not auth.autenticado or auth._perfil_id() not in roles:
            self.reset()
            raise api.XanoOperationError("Acesso não autorizado.")
        return auth

    async def _failure(self, exc: Exception):
        if isinstance(exc, api.XanoRejected):
            auth = await self.get_state(AuthState)
            auth._invalidar_sessao_rejeitada()
            self.reset()
            return rx.redirect("/login")
        else:
            self.error = (str(exc) if isinstance(exc, (ValueError, api.XanoOperationError, api.XanoConfigError))
                          else "Não foi possível concluir. Atualize para conferir os dados antes de tentar novamente.")

    async def _load(self, auth: AuthState):
        self.manager = auth._perfil_id() == 2
        self.ti_manager = self.manager and auth.perfil.get("departamento_id") == "1"
        token = auth.auth_token
        if self.section == "chamados" and self.manager:
            from .ticket_filters import reset_visible_filters
            reset_visible_filters(self._get_root_state())
            self.tickets = [_technical_ticket_view(r) for r in api.technician_tickets(token)]
        elif self.section in ("novo_chamado", "nova_tarefa", "usuarios") and self.manager:
            if self.section == "usuarios":
                deps = api.departments(token)
                allowed = {2, 3, 4} if self.ti_manager else {4}
                profiles = api.profiles(token)
                self.profile_options = option_rows([r for r in profiles if int(r["id"]) in allowed], "name")
                self.department_options = option_rows(deps if self.ti_manager else
                    [r for r in deps if str(r["id"]) == auth.perfil.get("departamento_id")])
                if not self.profile_options or not self.department_options:
                    raise ValueError("Perfis ou departamentos indisponíveis.")
                self.selected_profile = self.profile_options[0]["label"]
            else:
                self.priority_options = option_rows(api.list_priorities(token))
                if not self.priority_options:
                    raise ValueError("Nenhuma prioridade configurada.")
                if self.section == "novo_chamado":
                    self.category_options = option_rows(api.list_categories(token))
                    if not self.category_options:
                        raise ValueError("Nenhuma categoria configurada.")
                else:
                    profile = 3 if self.ti_manager else 4
                    self.owner_options = option_rows(api.directory(token, profile,
                        int(auth.perfil["departamento_id"])), "name")
        elif self.section == "tarefas" and auth._perfil_id() in (3, 4):
            rows = api.list_tasks(token)
            if any(auth.perfil.get("id") not in task_member_ids(r) for r in rows):
                raise api.XanoUnavailable("Escopo de tarefas inválido.")
            self.tasks = [public_task(r) for r in rows]

    @rx.event
    async def navigate(self, section: str):
        if self.saving or self.loading:
            return
        self.error = self.success = self.history_error = ""
        self.ticket = self.task = {}
        self.history = []
        self.solution = ""
        self.selected_owners = []
        self.owner_options = self.category_options = self.priority_options = []
        self.profile_options = self.department_options = []
        self.form_revision += 1
        try:
            auth = await self._auth()
            allowed = ("chamados", "novo_chamado", "nova_tarefa", "usuarios") if auth._perfil_id() == 2 else ("tarefas",)
            if section not in allowed:
                raise ValueError("Seção não autorizada.")
            self.section = section
            self.loading = True
            yield
            await self._load(auth)
        except ERRORS as exc:
            yield await self._failure(exc)
        finally:
            self.loading = False

    @rx.event
    async def initialize(self):
        self.reset()
        auth = await self.get_state(AuthState)
        if auth.autenticado and auth._perfil_id() in (2, 3, 4):
            self.manager = auth._perfil_id() == 2
            self.ti_manager = self.manager and auth.perfil.get("departamento_id") == "1"
            self.section = "chamados" if self.manager else "tarefas"
            self.loading = True
            yield
            try:
                await self._load(auth)
            except ERRORS as exc:
                yield await self._failure(exc)
            self.loading = False

    @rx.event
    async def view_ticket(self, ticket_id: str):
        if self.loading or self.saving:
            return
        self.ticket = {}
        self.history = []
        self.error = self.history_error = ""
        self.section = "detalhe"
        self.loading = True
        yield
        try:
            auth = await self._auth((2,))
            self.ticket = _technical_ticket_view(api.technician_ticket(int(ticket_id), auth.auth_token))
            try:
                self.history = [_interaction_view(r) for r in api.ticket_interactions(int(ticket_id), auth.auth_token)]
            except (api.XanoUnavailable, api.XanoOperationError):
                self.history_error = "Não foi possível carregar o histórico. Abra o chamado novamente para tentar."
        except ERRORS as exc:
            yield await self._failure(exc)
        self.loading = False

    @rx.event
    async def view_task(self, task_id: str):
        if self.loading or self.saving:
            return
        self.task = {}
        self.solution = self.error = self.success = ""
        self.section = "tarefa"
        self.loading = True
        yield
        try:
            auth = await self._auth((3, 4))
            row = api.get_task(auth.auth_token, int(task_id))
            if auth.perfil.get("id") not in task_member_ids(row):
                raise api.XanoOperationError("Tarefa não autorizada.")
            self.task = public_task(row)
            self.solution = self.task["solucao_aplicada"]
        except ERRORS as exc:
            yield await self._failure(exc)
        self.loading = False

    @rx.event
    async def submit(self, kind: str, form_data: dict):
        if self.saving or self.loading:
            return
        self.error = self.success = ""
        self.saving = True
        yield
        try:
            auth = await self._auth((3, 4) if kind == "concluir" else (2,))
            token = auth.auth_token
            if kind == "usuario":
                profile = option_id(self.profile_options, self.selected_profile)
                if not self.ti_manager and profile != 4:
                    raise ValueError("Perfil não autorizado.")
                dept = (1 if profile == 3 else option_id(self.department_options, str(form_data.get("departamento", ""))))
                name, email = (str(form_data.get(k, "")).strip() for k in ("name", "email"))
                password = str(form_data.get("password", ""))
                if not name or not email or len(password) < 8:
                    raise ValueError("Preencha nome, e-mail e senha válida.")
                created = api.provision_user(token, name, email, password, profile, dept)
            elif kind == "tarefa":
                title = str(form_data.get("titulo", "")).strip()
                if not title:
                    raise ValueError("Informe o título.")
                linked = str(form_data.get("chamado_id", "")).strip()
                if not self.selected_owners:
                    raise ValueError("Selecione pelo menos um responsável.")
                created = api.create_task(token, title, str(form_data.get("descricao", "")),
                    [option_id(self.owner_options, label) for label in self.selected_owners],
                    option_id(self.priority_options, str(form_data.get("prioridade", ""))),
                    str(form_data.get("prazo", "")), int(linked) if linked else None)
            elif kind == "chamado":
                title, description = (str(form_data.get(k, "")).strip() for k in ("titulo", "descricao"))
                if not title or not description:
                    raise ValueError("Preencha título e descrição.")
                created = api._record(api.office_request("POST", "chamado", token, payload={
                    "titulo": title, "descricao": description,
                    "categoria_chamado_id": option_id(self.category_options, str(form_data.get("categoria", ""))),
                    "prioridade_id": option_id(self.priority_options, str(form_data.get("prioridade", "")))}), "chamado")
            elif kind == "concluir":
                members = self.task.get("member_ids", "").split(",") if self.task.get("member_ids") else [self.task.get("responsavel_id")]
                if not self.task or auth.perfil.get("id") not in members:
                    raise ValueError("Tarefa não autorizada.")
                created = api.complete_task(token, int(self.task["id"]), self.solution)
                self.task = public_task(created)
                if self.task["concluido_em"]:
                    self.solution = self.task["solucao_aplicada"]
            else:
                raise ValueError("Operação inválida.")
            self.success = f"Operação salva com sucesso (#{created.get('id', '')})."
            if kind != "concluir":
                self.form_revision += 1
                self.selected_owners = []
        except ERRORS as exc:
            yield await self._failure(exc)
        finally:
            self.saving = False
        if kind == "usuario":
            yield rx.set_value("office_password", "")
        auth = await self.get_state(AuthState)
        if not auth.autenticado:
            yield rx.redirect("/login")
