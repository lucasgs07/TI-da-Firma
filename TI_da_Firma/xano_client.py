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
    token: str | None = None,
    client: httpx.Client | None = None,
) -> Any:
    url = f"{get_base_url()}/{path}"
    headers = auth_headers(token) if token else None
    try:
        if client is not None:
            response = client.request(method, url, json=json, headers=headers)
        else:
            with httpx.Client(timeout=TIMEOUT_SEGUNDOS) as http:
                response = http.request(method, url, json=json, headers=headers)
    except httpx.HTTPError as exc:
        raise XanoUnavailable("Não foi possível contatar o servidor.") from exc

    if response.status_code in (400, 401, 403):
        raise XanoRejected("Credenciais ou sessão rejeitadas.")
    if response.status_code != 200:
        logger.warning(
            "Xano %s %s respondeu %s: %s",
            method, path, response.status_code, response.text[:200],
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
