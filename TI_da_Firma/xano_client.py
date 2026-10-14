"""Cliente HTTP para os endpoints de autenticação do Xano."""

import logging
import os
from dataclasses import dataclass
from pathlib import Path

import httpx
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

BASE_URL_ENV = "XANO_API_BASE_URL"
TIMEOUT_SEGUNDOS = 15.0
USER_FIELDS = ("id", "name", "email", "perfil_id", "departamento_id")
PROJECT_ENV_FILE = Path(__file__).resolve().parent.parent / ".env"

load_dotenv(PROJECT_ENV_FILE)


class XanoConfigError(Exception):
    """A URL base da API do Xano não foi configurada."""


class XanoRejected(Exception):
    """O Xano rejeitou as credenciais ou o token (401/403)."""

    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self.status_code = status_code


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
) -> object:
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
        raise XanoRejected("Credenciais ou sessão rejeitadas.", response.status_code)
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
    token = data.get("authToken") if isinstance(data, dict) else None
    if not token:
        raise XanoUnavailable("Resposta inválida do servidor.")
    user = data.get("user")
    if not isinstance(user, dict):
        user = me(token, client)
    return LoginResult(auth_token=token, user=safe_user(user))


def me(token: str, client: httpx.Client | None = None) -> dict:
    return safe_user(_request("GET", "auth/me", token=token, client=client))


def get_ticket_categories(token: str, client: httpx.Client | None = None) -> list[dict]:
    data = _request("GET", "categoria_chamado", token=token, client=client)
    if not isinstance(data, list) or any(
        not isinstance(item, dict) or "id" not in item or "nome" not in item
        for item in data
    ):
        raise XanoUnavailable("Resposta inválida ao carregar as categorias.")
    return [{"id": item["id"], "nome": item["nome"]} for item in data]


def get_ticket_priorities(
    token: str, client: httpx.Client | None = None
) -> list[dict]:
    data = _request("GET", "prioridade", token=token, client=client)
    if not isinstance(data, list) or any(
        not isinstance(item, dict) or "id" not in item or "nome" not in item
        for item in data
    ):
        raise XanoUnavailable("Resposta inválida ao carregar as prioridades.")
    return [
        {"id": item["id"], "nome": item["nome"], "nivel": item.get("nivel")}
        for item in data
    ]


def create_ticket(
    token: str,
    *,
    titulo: str,
    descricao: str,
    categoria_chamado_id: int,
    prioridade_id: int,
    client: httpx.Client | None = None,
) -> dict:
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
    if not isinstance(data, dict):
        raise XanoUnavailable("Resposta inválida ao criar o chamado.")
    return data


def get_tickets(token: str, client: httpx.Client | None = None) -> list[dict]:
    data = _request("GET", "chamado", token=token, client=client)
    if not isinstance(data, list) or any(not isinstance(item, dict) for item in data):
        raise XanoUnavailable("Resposta inválida ao carregar os chamados.")
    return data


def get_ticket_interactions(
    token: str, client: httpx.Client | None = None
) -> list[dict]:
    data = _request("GET", "interacao_chamado", token=token, client=client)
    if not isinstance(data, list) or any(not isinstance(item, dict) for item in data):
        raise XanoUnavailable("Resposta inválida ao carregar as interações.")
    return data


def assume_ticket(
    token: str, ticket_id: int, client: httpx.Client | None = None
) -> dict:
    data = _request(
        "POST",
        f"chamado/{ticket_id}/assumir",
        token=token,
        client=client,
    )
    if not isinstance(data, dict):
        raise XanoUnavailable("Resposta inválida ao assumir o chamado.")
    return data


def update_ticket(
    token: str,
    ticket_id: int,
    *,
    status_nome: str | None = None,
    solucao_final: str | None = None,
    client: httpx.Client | None = None,
) -> dict:
    payload = {}
    if status_nome is not None:
        payload["status_nome"] = status_nome
    if solucao_final is not None:
        payload["solucao_final"] = solucao_final
    data = _request(
        "PATCH",
        f"chamado/{ticket_id}",
        json=payload,
        token=token,
        client=client,
    )
    if not isinstance(data, dict):
        raise XanoUnavailable("Resposta inválida ao atualizar o chamado.")
    return data


def create_ticket_interaction(
    token: str,
    ticket_id: int,
    mensagem: str,
    client: httpx.Client | None = None,
) -> dict:
    data = _request(
        "POST",
        "interacao_chamado",
        json={"chamado_id": ticket_id, "mensagem": mensagem},
        token=token,
        client=client,
    )
    if not isinstance(data, dict):
        raise XanoUnavailable("Resposta inválida ao registrar a interação.")
    return data
