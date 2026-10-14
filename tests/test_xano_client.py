"""Testes do cliente Xano com respostas simuladas."""

import httpx
import pytest

from TI_da_Firma import xano_client as xc

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
    with pytest.raises(xc.XanoRejected):
        xc.login("a", "b", client(lambda r: httpx.Response(403, json={})))


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


def test_listar_chamados_envia_token_e_usa_resposta_do_xano():
    ticket = {"id": 7, "titulo": "Notebook", "requester_name": "Ana"}

    def h(req):
        assert req.method == "GET"
        assert str(req.url) == "https://x.test/api:abc/chamado"
        assert req.headers["Authorization"] == "Bearer tok"
        return httpx.Response(200, json=[ticket])

    assert xc.list_tickets("tok", client(h)) == [ticket]


def test_consultar_chamado_usa_id_no_caminho():
    ticket = {"id": 7, "titulo": "Notebook"}

    def h(req):
        assert req.method == "GET"
        assert str(req.url) == "https://x.test/api:abc/chamado/7"
        assert req.headers["Authorization"] == "Bearer tok"
        return httpx.Response(200, json=ticket)

    assert xc.get_ticket(7, "tok", client(h)) == ticket


def test_consultar_chamado_rejeita_id_invalido_sem_requisicao():
    with pytest.raises(ValueError, match="positivo"):
        xc.get_ticket(0, "tok", client(lambda req: pytest.fail("Não deveria chamar a API")))


def test_criar_chamado_envia_somente_campos_editaveis():
    ticket = {"id": 8, "titulo": "Notebook", "solicitante_id": 3}

    def h(req):
        assert req.method == "POST"
        assert str(req.url) == "https://x.test/api:abc/chamado"
        assert req.headers["Authorization"] == "Bearer tok"
        assert req.read() == (
            b'{"titulo":"Notebook","descricao":"Nao liga",'
            b'"categoria_chamado_id":1,"prioridade_id":2}'
        )
        return httpx.Response(200, json=ticket)

    assert xc.create_ticket("Notebook", "Nao liga", 1, 2, "tok", client(h)) == ticket


def test_listar_lookups_preserva_ids_de_resposta():
    def h(req):
        assert req.method == "GET"
        assert req.headers["Authorization"] == "Bearer tok"
        if req.url.path.endswith("/categoria_chamado"):
            return httpx.Response(200, json=[{"id": 1, "nome": "Hardware"}])
        assert req.url.path.endswith("/prioridade")
        return httpx.Response(200, json=[{"id": 2, "nome": "Alta", "nivel": 1}])

    http = client(h)
    assert xc.list_categories("tok", http) == [{"id": "1", "nome": "Hardware"}]
    assert xc.list_priorities("tok", http) == [{"id": "2", "nome": "Alta"}]


@pytest.mark.parametrize(
    ("method_name", "response"),
    [
        ("list_tickets", {"id": 1}),
        ("list_categories", [{"nome": "Hardware"}]),
        ("list_priorities", [{"id": 1}]),
    ],
)
def test_respostas_invalidas_sao_reportadas(method_name, response):
    api_method = getattr(xc, method_name)
    with pytest.raises(xc.XanoUnavailable, match="Resposta inválida"):
        api_method("tok", client(lambda req: httpx.Response(200, json=response)))
