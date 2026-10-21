"""Cliente HTTP para os endpoints de autenticação do Xano."""

import logging
import os
from dataclasses import dataclass
from typing import Any

import httpx

logger = logging.getLogger(__name__)

BASE_URL_ENV = "XANO_API_BASE_URL"
TIMEOUT_SEGUNDOS = 15.0
USER_FIELDS = ("id", "name", "email", "perfil_id", "departamento_id")


class XanoConfigError(Exception):
    """A URL base da API do Xano não foi configurada."""


class XanoRejected(Exception):
    """O Xano rejeitou as credenciais ou o token (401/403)."""


class XanoUnavailable(Exception):
    """Falha de rede, timeout ou resposta inesperada do Xano."""


class XanoOperationError(Exception):
    """Requisição de atendimento negada ou inválida, sem invalidar a sessão."""


@dataclass(frozen=True)
class LoginResult:
    auth_token: str
    user: dict


def get_base_url() -> str:
    url = os.environ.get(BASE_URL_ENV, "").strip().rstrip("/")
    if not url:
        raise XanoConfigError(
            f"Variável de ambiente {BASE_URL_ENV} não configurada. "
            "Defina a URL base do grupo de API Authentication do Xano."
        )
    return url


def safe_user(data: object) -> dict:
    """Mantém somente os campos de usuário permitidos."""
    if not isinstance(data, dict):
        raise XanoUnavailable("Resposta inesperada do servidor.")
    return {field: data.get(field) for field in USER_FIELDS}


def auth_headers(token: str) -> dict[str, str]:
    """Cabeçalho para chamadas autenticadas ao Xano."""
    return {"Authorization": f"Bearer {token}"}


def _request(
    method: str,
    path: str,
    *,
    json: dict | None = None,
    params: dict | None = None,
    operational: bool = False,
    token: str | None = None,
    client: httpx.Client | None = None,
) -> Any:
    url = f"{get_base_url()}/{path}"
    headers = auth_headers(token) if token else None
    try:
        if client is not None:
            response = client.request(method, url, json=json, params=params, headers=headers)
        else:
            with httpx.Client(timeout=TIMEOUT_SEGUNDOS) as http:
                response = http.request(method, url, json=json, params=params, headers=headers)
    except httpx.HTTPError as exc:
        raise XanoUnavailable("Não foi possível contatar o servidor.") from exc

    if operational and response.status_code in (400, 403, 404, 409, 422):
        messages = {
            400: "Dados inválidos ou status não configurado. Revise a operação.",
            403: "Você não tem permissão para esta ação. Atualize o chamado.",
            404: "Chamado não encontrado ou indisponível para esta operação.",
            409: "O chamado foi alterado. Atualize antes de tentar novamente.",
            422: "Revise os dados e a configuração do status solicitado.",
        }
        raise XanoOperationError(messages[response.status_code])
    if response.status_code in (400, 401, 403):
        raise XanoRejected("Credenciais ou sessão rejeitadas.")
    if response.status_code != 200:
        logger.warning(
            "Xano %s %s respondeu %s",
            method, path, response.status_code,
        )
        raise XanoUnavailable("O servidor respondeu com erro inesperado.")
    try:
        return response.json()
    except ValueError as exc:
        raise XanoUnavailable("Resposta inválida do servidor.") from exc


def login(
    email: str, password: str, client: httpx.Client | None = None
) -> LoginResult:
    data = _request(
        "POST",
        "auth/login",
        json={"email": email, "password": password},
        client=client,
    )
    if not isinstance(data, dict):
        raise XanoUnavailable("Resposta inválida do servidor.")
    token = data.get("authToken")
    if not token:
        raise XanoUnavailable("Resposta inválida do servidor.")
    user = data.get("user")
    if not isinstance(user, dict):
        user = me(token, client)
    return LoginResult(auth_token=token, user=safe_user(user))


def me(token: str, client: httpx.Client | None = None) -> dict:
    return safe_user(_request("GET", "auth/me", token=token, client=client))


def _record_list(data: object, endpoint: str) -> list[dict]:
    if not isinstance(data, list) or any(not isinstance(record, dict) for record in data):
        raise XanoUnavailable(f"Resposta inválida ao consultar {endpoint}.")
    return data


def _record(data: object, endpoint: str) -> dict:
    if not isinstance(data, dict):
        raise XanoUnavailable(f"Resposta inválida ao consultar {endpoint}.")
    return data


def _lookup_list(data: object, endpoint: str) -> list[dict[str, str]]:
    records = _record_list(data, endpoint)
    options: list[dict[str, str]] = []
    for record in records:
        record_id = record.get("id")
        name = record.get("nome")
        if record_id is None or not name:
            raise XanoUnavailable(f"Resposta inválida ao consultar {endpoint}.")
        try:
            normalized_id = str(int(record_id))
        except (TypeError, ValueError) as exc:
            raise XanoUnavailable(f"Resposta inválida ao consultar {endpoint}.") from exc
        if int(normalized_id) < 1:
            raise XanoUnavailable(f"Resposta inválida ao consultar {endpoint}.")
        options.append({"id": normalized_id, "nome": str(name)})
    return options


def list_tickets(token: str, client: httpx.Client | None = None) -> list[dict]:
    """Lista chamados usando o escopo de visibilidade aplicado pelo Xano."""
    return _record_list(_request("GET", "chamado", token=token, client=client), "chamados")


def get_ticket(
    ticket_id: int, token: str, client: httpx.Client | None = None
) -> dict:
    """Consulta um chamado; o Xano decide se o usuário autenticado pode vê-lo."""
    if ticket_id < 1:
        raise ValueError("O identificador do chamado deve ser positivo.")
    data = _request("GET", f"chamado/{ticket_id}", token=token, client=client)
    return _record(data, "chamado")


def create_ticket(
    titulo: str,
    descricao: str,
    categoria_chamado_id: int,
    prioridade_id: int,
    token: str,
    client: httpx.Client | None = None,
) -> dict:
    """Cria chamado sem aceitar solicitante ou status definidos pelo cliente."""
    data = _request(
        "POST",
        "chamado",
        json={
            "titulo": titulo,
            "descricao": descricao,
            "categoria_chamado_id": categoria_chamado_id,
            "prioridade_id": prioridade_id,
        },
        token=token,
        client=client,
    )
    return _record(data, "criação do chamado")


def list_categories(
    token: str, client: httpx.Client | None = None
) -> list[dict[str, str]]:
    """Lista categorias disponíveis retornadas pelo Xano."""
    data = _request("GET", "categoria_chamado", token=token, client=client)
    return _lookup_list(data, "categorias")


def list_priorities(
    token: str, client: httpx.Client | None = None
) -> list[dict[str, str]]:
    """Lista prioridades disponíveis retornadas pelo Xano."""
    data = _request("GET", "prioridade", token=token, client=client)
    return _lookup_list(data, "prioridades")


def technician_tickets(token: str, client: httpx.Client | None = None) -> list[dict]:
    return _record_list(_request("GET", "chamado", token=token, client=client,
                                 operational=True), "chamados")


def ticket_statuses(token: str) -> list[dict[str, str]]:
    return _lookup_list(office_request("GET", "status_chamado", token), "status")


def search_tickets(token: str, priority_id: int | None = None,
                   status_id: int | None = None, requester: str = "",
                   client: httpx.Client | None = None) -> list[dict]:
    params: dict[str, str | int] = {}
    for key, value in (("prioridade_id", priority_id), ("status_chamado_id", status_id)):
        if value is not None:
            if type(value) is not int or value < 1:
                raise ValueError("Filtro inválido.")
            params[key] = value
    requester = requester.strip()
    if len(requester) > 200:
        raise ValueError("O nome do solicitante deve ter até 200 caracteres.")
    if requester:
        params["solicitante_nome"] = requester
    rows = _record_list(_request("GET", "chamado", token=token, params=params,
                                client=client, operational=True), "chamados")
    # Detect an outdated backend instead of silently displaying unfiltered data.
    if any((priority_id is not None and str(row.get("prioridade_id")) != str(priority_id))
           or (status_id is not None and str(row.get("status_chamado_id")) != str(status_id))
           or (requester and requester.casefold() not in str(row.get("requester_name") or "").casefold())
           for row in rows):
        raise XanoUnavailable("O servidor não aplicou os filtros. Verifique a publicação dos contratos.")
    return rows


def technician_ticket(ticket_id: int, token: str, client: httpx.Client | None = None) -> dict:
    _positive_ticket_id(ticket_id)
    return _record(_request("GET", f"chamado/{ticket_id}", token=token,
                            client=client, operational=True), "chamado")


def _positive_ticket_id(ticket_id: int) -> None:
    if ticket_id < 1:
        raise ValueError("O identificador do chamado deve ser positivo.")


def ticket_interactions(ticket_id: int, token: str, client: httpx.Client | None = None) -> list[dict]:
    _positive_ticket_id(ticket_id)
    data = _request("GET", "interacao_chamado", params={"chamado_id": ticket_id},
                    token=token, client=client, operational=True)
    rows = _record_list(data, "histórico")
    # Falhar se o servidor ignorar o novo filtro; não expor comentários de outro chamado.
    if any(str(row.get("chamado_id")) != str(ticket_id) for row in rows):
        raise XanoUnavailable("O servidor não aplicou o filtro do histórico.")
    return rows


def claim_ticket(ticket_id: int, token: str, client: httpx.Client | None = None) -> dict:
    _positive_ticket_id(ticket_id)
    return _record(_request("POST", f"chamado/{ticket_id}/assumir", token=token,
                            client=client, operational=True), "associação")


def comment_ticket(ticket_id: int, message: str, token: str,
                   client: httpx.Client | None = None) -> dict:
    _positive_ticket_id(ticket_id)
    if not message.strip():
        raise ValueError("Escreva um comentário.")
    return _record(_request("POST", "interacao_chamado",
                            json={"chamado_id": ticket_id, "mensagem": message.strip()},
                            token=token, client=client, operational=True), "comentário")


OPERATIONAL_STATUSES = ["Em Análise", "Em atendimento", "Aguardando usuário", "Resolvido", "Fechado"]


def update_ticket(ticket_id: int, status: str, solution: str, token: str,
                  client: httpx.Client | None = None) -> dict:
    _positive_ticket_id(ticket_id)
    if status not in OPERATIONAL_STATUSES:
        raise ValueError("Selecione um status válido.")
    if status in ("Resolvido", "Fechado") and not solution.strip():
        raise ValueError("Informe a solução final para resolver ou fechar o chamado.")
    payload = {"status_nome": status}
    if solution.strip():
        payload["solucao_final"] = solution.strip()
    return _record(_request("PATCH", f"chamado/{ticket_id}", json=payload,
                            token=token, client=client, operational=True), "atualização")


def office_request(method: str, path: str, token: str, *, payload: dict | None = None,
                   params: dict | None = None, client: httpx.Client | None = None):
    """Transporte autenticado; as funções abaixo limitam campos de escrita."""
    return _request(method, path, json=payload, params=params, token=token,
                    client=client, operational=True)


def departments(token: str) -> list[dict[str, str]]:
    return _lookup_list(office_request("GET", "departamento", token), "departamentos")


def profiles(token: str) -> list[dict]:
    return _record_list(office_request("GET", "perfil", token), "perfis")


def directory(token: str, profile_id: int, department_id: int) -> list[dict]:
    rows, page, seen = [], 1, set()
    while True:
        if page in seen:
            raise XanoUnavailable("Paginação inválida do diretório.")
        seen.add(page)
        data = _record(office_request("GET", "users/directory", token, params={
            "perfil_id": profile_id, "departamento_id": department_id,
            "page": page, "per_page": 100}), "diretório")
        batch = _record_list(data.get("items"), "diretório")
        if any(str(r.get("perfil_id")) != str(profile_id) or
               str(r.get("departamento_id")) != str(department_id) for r in batch):
            raise XanoUnavailable("O diretório não respeitou o escopo solicitado.")
        rows.extend(batch)
        next_page = data.get("nextPage")
        if not next_page:
            return rows
        try:
            page = int(next_page)
        except (ValueError, TypeError) as exc:
            raise XanoUnavailable("Paginação inválida do diretório.") from exc


ADMIN_USER_FIELDS = ("id", "name", "email", "perfil_id", "departamento_id", "status")


def _admin_user(data: object) -> dict:
    row = _record(data, "usuário")
    if type(row.get("id")) is not int or row["id"] < 1:
        raise XanoUnavailable("Resposta inválida ao consultar usuário.")
    return {key: row.get(key) for key in ADMIN_USER_FIELDS}


def admin_users(token: str, page: int = 1) -> dict:
    """Página global do diretório; autorização administrativa pertence ao Xano."""
    if type(page) is not int or page < 1:
        raise ValueError("Página inválida.")
    data = _record(office_request("GET", "users/directory", token,
                                  params={"page": page, "per_page": 50}), "usuários")
    items = [_admin_user(row) for row in _record_list(data.get("items"), "usuários")]
    ids = [row["id"] for row in items]
    next_page = data.get("nextPage") or 0
    total = data.get("itemsTotal")
    if (len(ids) != len(set(ids)) or len(ids) > 50 or type(total) is not int
            or total < len(items) or type(next_page) is not int
            or (next_page != 0 and next_page <= page)
            or (data.get("curPage") != page)):
        raise XanoUnavailable("Paginação inválida do diretório administrativo.")
    return {"items": items, "page": page, "next_page": next_page, "total": total}


def admin_user(token: str, user_id: int) -> dict:
    if type(user_id) is not int or user_id < 1:
        raise ValueError("Usuário inválido.")
    result = _admin_user(office_request("GET", f"users/{user_id}", token))
    if result["id"] != user_id:
        raise XanoUnavailable("O servidor retornou outro usuário.")
    return result


def edit_user(token: str, user_id: int, fields: dict) -> dict:
    allowed = set(ADMIN_USER_FIELDS) - {"id"}
    if (type(user_id) is not int or user_id < 1 or not fields
            or set(fields) - allowed):
        raise ValueError("Campos de edição inválidos.")
    if "status" in fields and fields["status"] not in ("Ativo", "Inativo"):
        raise ValueError("Status inválido.")
    if "perfil_id" in fields and (type(fields["perfil_id"]) is not int or fields["perfil_id"] not in (1, 2, 3, 4)):
        raise ValueError("Perfil inválido.")
    if "departamento_id" in fields and fields["departamento_id"] is not None and (
            type(fields["departamento_id"]) is not int or fields["departamento_id"] < 1):
        raise ValueError("Departamento inválido.")
    result = _admin_user(office_request("PATCH", f"users/{user_id}", token, payload=dict(fields)))
    if result["id"] != user_id:
        raise XanoUnavailable("O servidor retornou outro usuário.")
    return result


def provision_user(token: str, name: str, email: str, password: str,
                   profile_id: int, department_id: int) -> dict:
    return _record(office_request("POST", "users/create", token, payload={
        "name": name, "email": email, "password": password,
        "perfil_id": profile_id, "departamento_id": department_id}), "usuário")


def create_task(token: str, title: str, description: str, owner: int | list[int], priority: int,
                due: str = "", ticket_id: int | None = None) -> dict:
    payload = {"titulo": title, "descricao": description, "prioridade_id": priority}
    if isinstance(owner, list):
        if not owner or any(type(item) is not int or item < 1 for item in owner):
            raise ValueError("Selecione pelo menos um responsável válido.")
        payload["responsaveis_ids"] = list(dict.fromkeys(owner))
    else:
        if type(owner) is not int or owner < 1:
            raise ValueError("Selecione um responsável válido.")
        payload["responsavel_id"] = owner
    if due:
        payload["prazo"] = due
    if ticket_id is not None:
        payload["chamado_id"] = ticket_id
    return _record(office_request("POST", "tarefa", token, payload=payload), "tarefa")


def list_tasks(token: str) -> list[dict]:
    return _record_list(office_request("GET", "tarefa", token), "tarefas")


def get_task(token: str, task_id: int) -> dict:
    _positive_ticket_id(task_id)
    return _record(office_request("GET", f"tarefa/{task_id}", token), "tarefa")


def complete_task(token: str, task_id: int, solution: str) -> dict:
    _positive_ticket_id(task_id)
    if not solution.strip():
        raise ValueError("Informe a solução da tarefa.")
    return _record(office_request("PATCH", f"tarefa/{task_id}", token, payload={
        "status_nome": "Concluída", "solucao_aplicada": solution.strip()}), "conclusão")


def admin_metrics(token: str) -> dict[str, int]:
    data = _record(office_request("GET", "helpdesk/metrics/tickets", token), "indicadores")
    keys = ("abertos", "em_andamento", "finalizados", "nao_classificados", "total")
    if any(type(data.get(key)) is not int or data[key] < 0 for key in keys):
        raise XanoUnavailable("Indicadores inválidos.")
    if sum(data[key] for key in keys[:-1]) != data["total"]:
        raise XanoUnavailable("Indicadores inconsistentes.")
    return {key: data[key] for key in keys}


def admin_history(token: str, ticket_id: int | None = None, page: int = 1,
                  through_id: int | None = None) -> dict:
    if type(page) is not int or page < 1:
        raise ValueError("Página inválida.")
    params = {"page": page, "per_page": 100}
    if ticket_id is not None:
        if type(ticket_id) is not int or ticket_id < 1:
            raise ValueError("Chamado inválido.")
        params["chamado_id"] = ticket_id
    if through_id is not None:
        if type(through_id) is not int or through_id < 0:
            raise ValueError("Limite inválido.")
        params["through_id"] = through_id
    data = _record(office_request("GET", "helpdesk/tickets/history", token, params=params), "histórico")
    rows = _record_list(data.get("items"), "histórico")
    boundary = data.get("through_id")
    if type(boundary) is not int or boundary < 0 or (through_id is not None and boundary != through_id):
        raise XanoUnavailable("Limite inconsistente do histórico.")
    for row in rows:
        if (type(row.get("id")) is not int or not 0 < row["id"] <= boundary or
                (ticket_id is not None and str(row.get("chamado_id")) != str(ticket_id))):
            raise XanoUnavailable("Escopo inválido do histórico.")
    next_page = data.get("nextPage")
    if next_page is not None and (type(next_page) is not int or next_page <= page):
        raise XanoUnavailable("Paginação inválida do histórico.")
    return data


def admin_history_all(token: str, ticket_id: int | None = None) -> list[dict]:
    rows, seen, page, boundary = [], set(), 1, None
    while True:
        data = admin_history(token, ticket_id, page, boundary)
        boundary = data["through_id"]
        for row in data["items"]:
            if row["id"] not in seen:
                seen.add(row["id"])
                rows.append(row)
        next_page = data.get("nextPage")
        if next_page is None:
            expected = data.get("itemsTotal")
            if type(expected) is not int or expected != len(rows):
                raise XanoUnavailable("Histórico incompleto. Atualize e tente novamente.")
            return rows
        if type(next_page) is not int or next_page <= page:
            raise XanoUnavailable("Paginação inválida do histórico.")
        page = next_page
