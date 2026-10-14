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
