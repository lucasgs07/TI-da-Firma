"""Testes do cliente Xano com respostas simuladas."""

import json

import httpx
import pytest

from TI_da_Firma import xano_client as xc
from TI_da_Firma.auth_state import _rota_pos_login

USER = {"id": 1, "name": "Ana", "email": "a@x.com", "perfil_id": 2,
        "departamento_id": 3, "password": "segredo"}


def client(handler):
    return httpx.Client(transport=httpx.MockTransport(handler))


@pytest.fixture(autouse=True)
def base_url(monkeypatch):
    monkeypatch.setenv(xc.BASE_URL_ENV, "https://x.test/api:abc/")


def test_login_ok_filtra_campos():
    def h(req):
        assert str(req.url) == "https://x.test/api:abc/auth/login"
        return httpx.Response(200, json={"authToken": "tok", "user": USER})

    r = xc.login("a@x.com", "12345678", client(h))
    assert r.auth_token == "tok"
    assert set(r.user) == set(xc.USER_FIELDS)


def test_login_rejeitado():
    with pytest.raises(xc.XanoRejected) as error:
        xc.login("a", "b", client(lambda r: httpx.Response(403, json={})))
    assert error.value.status_code == 403


@pytest.mark.parametrize(
    ("perfil_id", "expected_route"),
    [(4, "/chamados/novo"), ("4", "/chamados/novo"), (1, "/"), (2, "/"), (3, "/")],
)
def test_rota_pos_login_apenas_para_funcionario(perfil_id, expected_route):
    assert _rota_pos_login(perfil_id) == expected_route


def test_rede_falha():
    def h(req):
        raise httpx.ConnectError("x")

    with pytest.raises(xc.XanoUnavailable):
        xc.me("tok", client(h))


def test_me_envia_header_bearer():
    def h(req):
        assert req.headers["Authorization"] == "Bearer tok"
        assert "tok" not in str(req.url)
        return httpx.Response(200, json=USER)

    assert xc.me("tok", client(h))["perfil_id"] == 2


def test_me_token_rejeitado():
    with pytest.raises(xc.XanoRejected):
        xc.me("tok", client(lambda r: httpx.Response(401)))


def test_url_ausente(monkeypatch):
    monkeypatch.delenv(xc.BASE_URL_ENV)
    with pytest.raises(xc.XanoConfigError):
        xc.me("tok")


def test_carrega_categorias_com_autenticacao():
    def handler(request):
        assert request.method == "GET"
        assert str(request.url) == "https://x.test/api:abc/categoria_chamado"
        assert request.headers["Authorization"] == "Bearer tok"
        return httpx.Response(200, json=[{"id": 7, "nome": "Acesso"}])

    assert xc.get_ticket_categories("tok", client(handler)) == [
        {"id": 7, "nome": "Acesso"}
    ]


def test_carrega_prioridades_com_autenticacao():
    def handler(request):
        assert request.method == "GET"
        assert str(request.url) == "https://x.test/api:abc/prioridade"
        assert request.headers["Authorization"] == "Bearer tok"
        return httpx.Response(200, json=[{"id": 2, "nome": "Alta", "nivel": 1}])

    assert xc.get_ticket_priorities("tok", client(handler)) == [
        {"id": 2, "nome": "Alta", "nivel": 1}
    ]


def test_cria_chamado_sem_enviar_identidade_ou_status():
    expected_payload = {
        "titulo": "Impressora indisponível",
        "descricao": "A impressora do setor não responde.",
        "categoria_chamado_id": 7,
        "prioridade_id": 2,
    }

    def handler(request):
        assert request.method == "POST"
        assert str(request.url) == "https://x.test/api:abc/chamado"
        assert request.headers["Authorization"] == "Bearer tok"
        assert request.read()
        assert json.loads(request.content) == expected_payload
        return httpx.Response(
            200,
            json={
                "id": 55,
                "titulo": expected_payload["titulo"],
                "solicitante_id": 9,
                "solicitante_nome": "Ana",
                "status_nome": "Aberto",
            },
        )

    assert xc.create_ticket("tok", **expected_payload, client=client(handler))["id"] == 55


def test_lista_chamados_envia_autenticacao():
    def handler(request):
        assert request.method == "GET"
        assert str(request.url) == "https://x.test/api:abc/chamado"
        assert request.headers["Authorization"] == "Bearer tok"
        return httpx.Response(200, json=[{"id": 55, "titulo": "Impressora"}])

    assert xc.get_tickets("tok", client(handler)) == [
        {"id": 55, "titulo": "Impressora"}
    ]


def test_lista_interacoes_envia_autenticacao():
    def handler(request):
        assert request.method == "GET"
        assert str(request.url) == "https://x.test/api:abc/interacao_chamado"
        assert request.headers["Authorization"] == "Bearer tok"
        return httpx.Response(200, json=[{"id": 3, "chamado_id": 55, "mensagem": "Análise"}])

    assert xc.get_ticket_interactions("tok", client(handler))[0]["chamado_id"] == 55


def test_assume_chamado_envia_autenticacao():
    def handler(request):
        assert request.method == "POST"
        assert str(request.url) == "https://x.test/api:abc/chamado/55/assumir"
        assert request.headers["Authorization"] == "Bearer tok"
        return httpx.Response(200, json={"id": 55, "status_nome": "Aberto"})

    assert xc.assume_ticket("tok", 55, client(handler))["id"] == 55


def test_atualiza_chamado_envia_somente_campos_operacionais():
    expected_payload = {
        "status_nome": "Em atendimento",
        "solucao_final": "",
    }

    def handler(request):
        assert request.method == "PATCH"
        assert str(request.url) == "https://x.test/api:abc/chamado/55"
        assert request.headers["Authorization"] == "Bearer tok"
        assert json.loads(request.content) == expected_payload
        return httpx.Response(200, json={"id": 55, "status_nome": "Em atendimento"})

    assert xc.update_ticket(
        "tok",
        55,
        status_nome="Em atendimento",
        solucao_final="",
        client=client(handler),
    )["status_nome"] == "Em atendimento"


def test_cria_interacao_envia_mensagem_e_ticket():
    expected_payload = {"chamado_id": 55, "mensagem": "Estou verificando."}

    def handler(request):
        assert request.method == "POST"
        assert str(request.url) == "https://x.test/api:abc/interacao_chamado"
        assert request.headers["Authorization"] == "Bearer tok"
        assert json.loads(request.content) == expected_payload
        return httpx.Response(200, json={"id": 4, **expected_payload})

    assert xc.create_ticket_interaction(
        "tok", 55, "Estou verificando.", client(handler)
    )["id"] == 4
