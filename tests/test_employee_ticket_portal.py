import json

import httpx
import pytest

from TI_da_Firma import auth_state
from TI_da_Firma import xano_client
from TI_da_Firma.auth_state import AuthState, _ticket_view

EXPECTED_CATEGORY_ROWS = [
    {"id": "1", "nome": "Hardware"},
    {"id": "2", "nome": "Software"},
    {"id": "3", "nome": "Rede"},
    {"id": "4", "nome": "Acesso"},
    {"id": "5", "nome": "Impressora"},
    {"id": "6", "nome": "Outros"},
]


@pytest.fixture
def employee_state():
    state = AuthState(_reflex_internal_init=True)
    state.autenticado = True
    state.auth_token = "test-token"
    state.perfil_json = json.dumps({"perfil_id": 4})
    return state


def test_ticket_view_normalizes_api_fields_and_omits_unneeded_fields():
    ticket = _ticket_view(
        {
            "id": 12,
            "titulo": "Acesso ao sistema",
            "descricao": "Não consigo entrar",
            "status_name": "Aberto",
            "category_name": "Acesso",
            "priority_name": "Alta",
            "solicitante_id": 99,
            "password": "not returned",
        }
    )

    assert ticket == {
        "id": "12",
        "titulo": "Acesso ao sistema",
        "descricao": "Não consigo entrar",
        "status_name": "Aberto",
        "category_name": "Acesso",
        "priority_name": "Alta",
    }


def test_ticket_view_supports_create_response_field_names():
    ticket = _ticket_view(
        {
            "id": 13,
            "titulo": "Impressora",
            "descricao": "Falha ao imprimir",
            "status_nome": "Aberto",
            "categoria_nome": "Impressora",
            "prioridade_nome": "Normal",
        }
    )

    assert ticket["status_name"] == "Aberto"
    assert ticket["category_name"] == "Impressora"
    assert ticket["priority_name"] == "Normal"


def test_lista_de_chamados_carrega_resultados_e_estado_vazio(
    employee_state, monkeypatch
):
    monkeypatch.setattr(
        auth_state.xano_client,
        "list_tickets",
        lambda token: [{"id": 4, "titulo": "Impressora"}],
    )
    list(AuthState.atualizar_chamados.fn(employee_state))

    assert employee_state.chamados == [
        {
            "id": "4",
            "titulo": "Impressora",
            "descricao": "",
            "status_name": "",
            "category_name": "",
            "priority_name": "",
        }
    ]
    assert not employee_state.carregando_chamados

    monkeypatch.setattr(auth_state.xano_client, "list_tickets", lambda token: [])
    list(AuthState.atualizar_chamados.fn(employee_state))
    assert employee_state.chamados == []
    assert not employee_state.erro_chamados


def test_erro_de_lista_e_reportado_sem_sucesso_falso(employee_state, monkeypatch):
    def unavailable(token):
        raise auth_state.xano_client.XanoUnavailable("offline")

    monkeypatch.setattr(auth_state.xano_client, "list_tickets", unavailable)
    list(AuthState.atualizar_chamados.fn(employee_state))

    assert employee_state.erro_chamados
    assert not employee_state.carregando_chamados


def test_sessao_rejeitada_limpa_chamados_e_perfil(employee_state, monkeypatch):
    employee_state.chamados = [{"id": "2", "titulo": "Chamado privado"}]

    def rejected(token):
        raise auth_state.xano_client.XanoRejected("expired")

    monkeypatch.setattr(
        auth_state.xano_client,
        "list_tickets",
        rejected,
    )

    list(AuthState.atualizar_chamados.fn(employee_state))

    assert not employee_state.autenticado
    assert not employee_state.auth_token
    assert employee_state.chamados == []
    assert employee_state.erro_rede


def test_detalhe_negado_limpa_dados_anteriores(employee_state, monkeypatch):
    employee_state.chamado_atual = {"id": "3", "titulo": "Dados antigos"}

    def unavailable(ticket_id, token):
        raise auth_state.xano_client.XanoUnavailable("not found")

    monkeypatch.setattr(auth_state.xano_client, "get_ticket", unavailable)
    list(AuthState.ver_chamado.fn(employee_state, "9"))

    assert employee_state.chamado_atual == {}
    assert employee_state.erro_chamados
    assert not employee_state.carregando_chamados


def test_detalhe_proprio_exibe_somente_campos_permitidos(employee_state, monkeypatch):
    monkeypatch.setattr(
        auth_state.xano_client,
        "get_ticket",
        lambda ticket_id, token: {
            "id": ticket_id,
            "titulo": "Chamado próprio",
            "descricao": "Descrição",
            "status_name": "Aberto",
            "category_name": "Rede",
            "priority_name": "Alta",
            "solicitante_id": 999,
        },
    )
    list(AuthState.ver_chamado.fn(employee_state, "9"))

    assert employee_state.chamado_atual["titulo"] == "Chamado próprio"
    assert "solicitante_id" not in employee_state.chamado_atual
    assert not employee_state.erro_chamados


def test_outro_perfil_nao_dispara_consulta_de_chamados(monkeypatch):
    state = AuthState(_reflex_internal_init=True)
    state.autenticado = True
    state.perfil_json = json.dumps({"perfil_id": 3})
    monkeypatch.setattr(
        auth_state.xano_client,
        "list_tickets",
        lambda token: pytest.fail("Perfil não autorizado chamou a API"),
    )

    list(AuthState.atualizar_chamados.fn(state))

    assert state.erro_chamados == "Acesso não autorizado."
    assert state.chamados == []


def test_outro_perfil_nao_abre_formulario_funcionario(monkeypatch):
    state = AuthState(_reflex_internal_init=True)
    state.autenticado = True
    state.perfil_json = json.dumps({"perfil_id": 2})
    monkeypatch.setattr(
        auth_state.xano_client,
        "list_categories",
        lambda token: pytest.fail("Perfil não autorizado carregou opções"),
    )

    list(AuthState.mostrar_formulario_chamado.fn(state))

    assert state.erro_chamados == "Acesso não autorizado."
    assert state.tela_funcionario == "lista"


def test_formulario_carrega_categorias_e_prioridades_da_api(
    employee_state, monkeypatch
):
    monkeypatch.setattr(
        auth_state.xano_client,
        "list_categories",
        lambda token: EXPECTED_CATEGORY_ROWS,
    )
    monkeypatch.setattr(
        auth_state.xano_client,
        "list_priorities",
        lambda token: [{"id": "12", "nome": "Alta"}],
    )

    list(AuthState.mostrar_formulario_chamado.fn(employee_state))

    assert employee_state.categorias == EXPECTED_CATEGORY_ROWS
    assert employee_state.prioridades == [{"id": "12", "nome": "Alta"}]
    assert not employee_state.erro_chamados
    assert not employee_state.carregando_opcoes


def test_formulario_bloqueia_abertura_quando_lookup_falha(
    employee_state, monkeypatch
):
    monkeypatch.setattr(
        auth_state.xano_client,
        "list_categories",
        lambda token: EXPECTED_CATEGORY_ROWS,
    )

    def unavailable(token):
        raise auth_state.xano_client.XanoUnavailable("offline")

    monkeypatch.setattr(auth_state.xano_client, "list_priorities", unavailable)
    list(AuthState.mostrar_formulario_chamado.fn(employee_state))

    assert employee_state.erro_chamados
    assert employee_state.categorias == []
    assert employee_state.prioridades == []
    assert not employee_state.carregando_opcoes


def test_formulario_aceita_categorias_validas_retorna_xano(
    employee_state, monkeypatch
):
    categories = [
        {"id": "31", "nome": "Rede"},
        {"id": "32", "nome": "Outros"},
    ]
    monkeypatch.setattr(
        auth_state.xano_client, "list_categories", lambda token: categories
    )
    monkeypatch.setattr(
        auth_state.xano_client,
        "list_priorities",
        lambda token: [{"id": "12", "nome": "Alta"}],
    )

    list(AuthState.mostrar_formulario_chamado.fn(employee_state))

    assert employee_state.categorias == categories
    assert not employee_state.erro_chamados
    assert employee_state.opcoes_chamado_validas


def test_abertura_usa_ids_das_opcoes_retornadas(employee_state, monkeypatch):
    employee_state.categorias = [{"id": "31", "nome": "Rede"}]
    employee_state.prioridades = [{"id": "12", "nome": "Alta"}]
    captured = {}

    def create_ticket(titulo, descricao, categoria_id, prioridade_id, token):
        captured.update(
            {
                "titulo": titulo,
                "descricao": descricao,
                "categoria_id": categoria_id,
                "prioridade_id": prioridade_id,
                "token": token,
            }
        )
        return {"id": 21}

    monkeypatch.setattr(auth_state.xano_client, "create_ticket", create_ticket)
    monkeypatch.setattr(auth_state.xano_client, "list_tickets", lambda token: [])
    list(
        AuthState.abrir_chamado.fn(
            employee_state,
            {
                "titulo": "Sem acesso",
                "descricao": "Falha de login",
                "categoria": "Rede",
                "prioridade": "Alta",
            },
        )
    )

    assert captured == {
        "titulo": "Sem acesso",
        "descricao": "Falha de login",
        "categoria_id": 31,
        "prioridade_id": 12,
        "token": "test-token",
    }
    assert employee_state.sucesso_chamado == "Chamado #21 aberto com sucesso."
    assert not employee_state.erro_chamados


def test_abertura_invalida_nao_chama_api(employee_state, monkeypatch):
    monkeypatch.setattr(
        auth_state.xano_client,
        "create_ticket",
        lambda *args: pytest.fail("Formulário inválido chamou a API"),
    )
    employee_state.categorias = EXPECTED_CATEGORY_ROWS
    employee_state.prioridades = [{"id": "12", "nome": "Alta"}]

    list(
        AuthState.abrir_chamado.fn(
            employee_state,
            {
                "titulo": "",
                "descricao": "Descrição",
                "categoria": "Acesso",
                "prioridade": "Alta",
            },
        )
    )

    assert employee_state.erro_chamados
    assert not employee_state.sucesso_chamado
    assert not employee_state.enviando_chamado


def test_falha_de_abertura_nao_anuncia_sucesso(employee_state, monkeypatch):
    employee_state.categorias = EXPECTED_CATEGORY_ROWS
    employee_state.prioridades = [{"id": "12", "nome": "Alta"}]

    def rejected(*args):
        raise auth_state.xano_client.XanoRejected("rejected")

    monkeypatch.setattr(auth_state.xano_client, "create_ticket", rejected)
    list(
        AuthState.abrir_chamado.fn(
            employee_state,
            {
                "titulo": "Acesso",
                "descricao": "Sem acesso",
                "categoria": "Acesso",
                "prioridade": "Alta",
            },
        )
    )

    assert employee_state.erro
    assert employee_state.erro_rede
    assert not employee_state.sucesso_chamado
    assert not employee_state.enviando_chamado


def test_indisponibilidade_na_abertura_preserva_sessao_e_nao_confirma(
    employee_state, monkeypatch
):
    employee_state.categorias = EXPECTED_CATEGORY_ROWS
    employee_state.prioridades = [{"id": "12", "nome": "Alta"}]

    def unavailable(*args):
        raise auth_state.xano_client.XanoUnavailable("offline")

    monkeypatch.setattr(auth_state.xano_client, "create_ticket", unavailable)
    list(
        AuthState.abrir_chamado.fn(
            employee_state,
            {
                "titulo": "Acesso",
                "descricao": "Sem acesso",
                "categoria": "Acesso",
                "prioridade": "Alta",
            },
        )
    )

    assert employee_state.autenticado
    assert employee_state.erro_chamados
    assert not employee_state.sucesso_chamado
    assert not employee_state.enviando_chamado


def test_fluxo_completo_com_api_xano_simulada(employee_state, monkeypatch):
    requests = []
    ticket = {
        "id": 21,
        "titulo": "Acesso",
        "descricao": "Sem acesso",
        "status_name": "Aberto",
        "category_name": "Acesso",
        "priority_name": "Alta",
    }

    def handler(request):
        requests.append(request)
        assert request.headers["Authorization"] == "Bearer test-token"
        path = request.url.path
        if path == "/api:abc/categoria_chamado":
            return httpx.Response(200, json=EXPECTED_CATEGORY_ROWS)
        if path == "/api:abc/prioridade":
            return httpx.Response(200, json=[{"id": 12, "nome": "Alta"}])
        if path == "/api:abc/chamado" and request.method == "POST":
            assert json.loads(request.content) == {
                "titulo": "Acesso",
                "descricao": "Sem acesso",
                "categoria_chamado_id": 4,
                "prioridade_id": 12,
            }
            return httpx.Response(200, json={**ticket, "solicitante_id": 4})
        if path == "/api:abc/chamado" and request.method == "GET":
            return httpx.Response(200, json=[ticket])
        if path == "/api:abc/chamado/21":
            return httpx.Response(200, json=ticket)
        if path == "/api:abc/chamado/22":
            return httpx.Response(404, json={"message": "not found"})
        pytest.fail(f"Endpoint inesperado: {request.method} {path}")

    transport = httpx.MockTransport(handler)

    class ReusableClient(httpx.Client):
        def __exit__(self, *args):
            return False

    monkeypatch.setenv(xano_client.BASE_URL_ENV, "https://x.test/api:abc")
    monkeypatch.setattr(
        xano_client.httpx,
        "Client",
        lambda **kwargs: ReusableClient(transport=transport, **kwargs),
    )

    list(AuthState.mostrar_formulario_chamado.fn(employee_state))
    list(
        AuthState.abrir_chamado.fn(
            employee_state,
            {
                "titulo": "Acesso",
                "descricao": "Sem acesso",
                "categoria": "Acesso",
                "prioridade": "Alta",
            },
        )
    )
    list(AuthState.ver_chamado.fn(employee_state, "21"))

    assert employee_state.chamado_atual["id"] == "21"
    assert employee_state.chamado_atual["category_name"] == "Acesso"

    list(AuthState.ver_chamado.fn(employee_state, "22"))
    assert employee_state.chamado_atual == {}
    assert employee_state.erro_chamados
    assert len(requests) == 6


def test_login_e_validacao_de_sessao_preservam_contexto_seguro(monkeypatch):
    state = AuthState(_reflex_internal_init=True)
    user = {
        "id": 5,
        "name": "Funcionário",
        "email": "employee@example.test",
        "perfil_id": 2,
        "departamento_id": 7,
    }
    monkeypatch.setattr(
        auth_state.xano_client,
        "login",
        lambda email, password: xano_client.LoginResult("session-token", user),
    )
    list(
        AuthState.entrar.fn(
            state,
            {"email": "employee@example.test", "password": "secret"},
        )
    )

    assert state.auth_token == "session-token"
    assert state.autenticado
    assert state.perfil["perfil_id"] == "2"

    monkeypatch.setattr(auth_state.xano_client, "me", lambda token: user)
    list(AuthState.verificar_sessao.fn(state))
    assert state.autenticado
    assert state.perfil["departamento_id"] == "7"


def test_logout_limpa_sessao_e_dados_de_chamados():
    state = AuthState(_reflex_internal_init=True)
    state.auth_token = "session-token"
    state.perfil_json = json.dumps({"perfil_id": 4})
    state.autenticado = True
    state.chamados = [{"id": "8", "titulo": "Privado"}]

    AuthState.sair.fn(state)

    assert not state.auth_token
    assert not state.perfil_json
    assert not state.autenticado
    assert state.chamados == []
