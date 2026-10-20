import json

import httpx
import pytest

from TI_da_Firma.auth_state import AuthState, _technical_ticket_view
from TI_da_Firma import xano_client as xc


@pytest.fixture
def state():
    s = AuthState(_reflex_internal_init=True)
    s.autenticado = True
    s.auth_token = "test-token"
    s.perfil_json = json.dumps({"id": 30, "perfil_id": 3})
    return s


def ticket(status="Aberto", assigned=True):
    return {"id": 12, "titulo": "Impressora", "descricao": "Não imprime",
            "status_name": status, "requester_name": "Ana", "solicitante_id": 99,
            "tecnicos": [{"id": 30, "name": "Técnico"}] if assigned else [{"id": 31, "name": "Outro"}]}


def install_api(monkeypatch, row=None):
    row = row or ticket()
    monkeypatch.setattr(xc, "technician_ticket", lambda *a: row)
    monkeypatch.setattr(xc, "technician_tickets", lambda *a: [row])
    monkeypatch.setattr(xc, "ticket_interactions", lambda *a: [])


@pytest.mark.parametrize("status", ["Aberto", "Em atendimento", "Resolvido", "Fechado"])
def test_leitura_global_inclui_outro_tecnico_e_finalizados(state, monkeypatch, status):
    install_api(monkeypatch, ticket(status, assigned=False))
    list(AuthState.atualizar_lista_tecnica.fn(state))
    list(AuthState.abrir_atendimento.fn(state, "12"))
    assert state.chamados_tecnicos[0]["id"] == "12"
    assert state.atendimento["solicitante_id"] == "99"
    assert state.atendimento["requester_name"] == "Ana"
    assert not state.tecnico_associado
    assert not state.pode_atualizar_atendimento
    assert state.pode_associar == (status == "Aberto")


@pytest.mark.parametrize("profile", [1, 2, 4])
def test_outros_perfis_nao_carregam_area_tecnica(state, monkeypatch, profile):
    state.perfil_json = json.dumps({"id": 30, "perfil_id": profile})
    monkeypatch.setattr(xc, "technician_tickets", lambda *a: pytest.fail("Acesso técnico indevido"))
    list(AuthState.atualizar_lista_tecnica.fn(state))
    list(AuthState.abrir_atendimento.fn(state, "12"))
    assert not state.atendimento


def test_restauracao_valida_perfil_pelo_servidor_e_limpa_rascunhos(state, monkeypatch):
    state.comentario = "antigo"
    install_api(monkeypatch)
    monkeypatch.setattr(xc, "me", lambda token: {"id": 30, "perfil_id": 3})
    list(AuthState.verificar_sessao.fn(state))
    assert state.autenticado
    assert state.chamados_tecnicos
    assert state.comentario == ""


def test_troca_chamado_limpa_dados_e_erro_historico_independente(state, monkeypatch):
    install_api(monkeypatch)
    state.comentario = "rascunho anterior"
    state.historico = [{"mensagem": "antigo"}]

    def fail(*a):
        raise xc.XanoUnavailable()

    monkeypatch.setattr(xc, "ticket_interactions", fail)
    list(AuthState.abrir_atendimento.fn(state, "12"))
    assert state.atendimento["id"] == "12"
    assert state.comentario == ""
    assert not state.historico
    assert state.erro_historico
    assert not state.erro_tecnico


def test_chamado_inexistente_nao_exibe_dados_anteriores(state, monkeypatch):
    state.atendimento = {"id": "1"}

    def fail(*a):
        raise xc.XanoOperationError("Chamado não encontrado")

    monkeypatch.setattr(xc, "technician_ticket", fail)
    list(AuthState.abrir_atendimento.fn(state, "999"))
    assert state.atendimento == {}
    assert "não encontrado" in state.erro_tecnico
    assert state.autenticado


@pytest.mark.parametrize("action,method", [("associar", "claim_ticket"), ("comentar", "comment_ticket"), ("status", "update_ticket")])
def test_escrita_recarrega_detalhe_lista_historico(state, monkeypatch, action, method):
    install_api(monkeypatch, ticket(assigned=action != "associar"))
    list(AuthState.abrir_atendimento.fn(state, "12"))
    state.comentario = "Comentário"
    state.solucao = "Solução"
    state.status_destino = "Resolvido"
    calls = []
    monkeypatch.setattr(xc, method, lambda *args: calls.append(args) or {"id": 12})
    list(AuthState.executar_atendimento.fn(state, action))
    assert len(calls) == 1
    assert calls[0][0] == 12
    assert calls[0][-1] == "test-token"
    assert state.sucesso_tecnico
    assert not state.enviando_atendimento
    assert state.chamados_tecnicos


def test_rejeicao_preserva_texto_e_nao_encerra_sessao(state, monkeypatch):
    install_api(monkeypatch)
    list(AuthState.abrir_atendimento.fn(state, "12"))
    state.comentario = "Meu texto"

    def deny(*a):
        raise xc.XanoOperationError("Sem permissão")

    monkeypatch.setattr(xc, "comment_ticket", deny)
    list(AuthState.executar_atendimento.fn(state, "comentar"))
    assert state.comentario == "Meu texto"
    assert state.autenticado
    assert state.erro_tecnico == "Sem permissão"
    assert not state.sucesso_tecnico


def test_envio_duplo_e_navegacao_durante_escrita_sao_bloqueados(state, monkeypatch):
    install_api(monkeypatch)
    list(AuthState.abrir_atendimento.fn(state, "12"))
    state.enviando_atendimento = True
    monkeypatch.setattr(xc, "comment_ticket", lambda *a: pytest.fail("Envio duplicado"))
    list(AuthState.executar_atendimento.fn(state, "comentar"))
    list(AuthState.abrir_atendimento.fn(state, "99"))
    AuthState.voltar_lista_tecnica.fn(state)
    assert state.atendimento["id"] == "12"


def test_tecnico_nao_associado_nao_comenta_nem_atualiza(state, monkeypatch):
    install_api(monkeypatch, ticket(assigned=False))
    list(AuthState.abrir_atendimento.fn(state, "12"))
    monkeypatch.setattr(xc, "comment_ticket", lambda *a: pytest.fail("Escrita indevida"))
    monkeypatch.setattr(xc, "update_ticket", lambda *a: pytest.fail("Escrita indevida"))
    list(AuthState.executar_atendimento.fn(state, "comentar"))
    list(AuthState.executar_atendimento.fn(state, "status"))
    assert state.erro_tecnico


def test_associacao_legada_so_quando_nao_ha_relacoes(state, monkeypatch):
    row = ticket(assigned=False)
    row["responsavel_id"] = 30
    install_api(monkeypatch, row)
    list(AuthState.abrir_atendimento.fn(state, "12"))
    assert not state.tecnico_associado
    del row["tecnicos"]
    list(AuthState.abrir_atendimento.fn(state, "12"))
    assert state.tecnico_associado


@pytest.mark.parametrize("status", ["Resolvido", "Fechado"])
def test_concluido_bloqueia_operacao_mas_preserva_comentarios(state, monkeypatch, status):
    install_api(monkeypatch, ticket(status))
    list(AuthState.abrir_atendimento.fn(state, "12"))
    assert state.tecnico_associado
    assert not state.pode_atualizar_atendimento
    assert not state.pode_associar


def test_sessao_expirada_limpa_dados_e_redireciona(state, monkeypatch):
    install_api(monkeypatch)
    list(AuthState.abrir_atendimento.fn(state, "12"))

    def expired(*a):
        raise xc.XanoRejected()

    monkeypatch.setattr(xc, "comment_ticket", expired)
    result = list(AuthState.executar_atendimento.fn(state, "comentar"))
    assert not state.autenticado
    assert not state.atendimento
    assert not state.chamados_tecnicos
    assert not state.auth_token
    assert result[-1] is not None


def test_logout_limpa_toda_area_tecnica(state):
    state.chamados_tecnicos = [{"id": "12"}]
    state.atendimento = {"id": "12"}
    state.comentario = "privado"
    AuthState.sair.fn(state)
    assert not state.chamados_tecnicos and not state.atendimento and not state.comentario


def test_projecao_tecnica_nao_repassa_campos_privados():
    row = ticket()
    row["password"] = "segredo"
    assert "password" not in _technical_ticket_view(row)


@pytest.mark.parametrize("operation,verb,path,payload", [
    (lambda h: xc.claim_ticket(12, "token", h), "POST", "/chamado/12/assumir", None),
    (lambda h: xc.comment_ticket(12, " Texto ", "token", h), "POST", "/interacao_chamado", {"chamado_id": 12, "mensagem": "Texto"}),
    (lambda h: xc.update_ticket(12, "Resolvido", " Resolvido ", "token", h), "PATCH", "/chamado/12", {"status_nome": "Resolvido", "solucao_final": "Resolvido"}),
])
def test_contratos_http_sem_identidade_editavel(monkeypatch, operation, verb, path, payload):
    monkeypatch.setenv(xc.BASE_URL_ENV, "https://x.test")

    def handle(req):
        assert req.method == verb and req.url.path == path
        assert req.headers["Authorization"] == "Bearer token"
        assert (json.loads(req.content) if req.content else None) == payload
        return httpx.Response(200, json={"id": 12})

    with httpx.Client(transport=httpx.MockTransport(handle)) as h:
        operation(h)


def test_historico_filtra_no_servidor_e_rejeita_resposta_sem_filtro(monkeypatch):
    monkeypatch.setenv(xc.BASE_URL_ENV, "https://x.test")

    def handle(req):
        assert req.url.params["chamado_id"] == "12"
        return httpx.Response(200, json=[{"id": 1, "chamado_id": 99}])

    with httpx.Client(transport=httpx.MockTransport(handle)) as h:
        with pytest.raises(xc.XanoUnavailable, match="filtro"):
            xc.ticket_interactions(12, "token", h)


@pytest.mark.parametrize("code,error", [(400, xc.XanoOperationError), (403, xc.XanoOperationError),
                                        (404, xc.XanoOperationError), (409, xc.XanoOperationError),
                                        (422, xc.XanoOperationError), (401, xc.XanoRejected),
                                        (500, xc.XanoUnavailable)])
def test_classificacao_erros_operacionais(monkeypatch, code, error):
    monkeypatch.setenv(xc.BASE_URL_ENV, "https://x.test")
    with httpx.Client(transport=httpx.MockTransport(lambda req: httpx.Response(code))) as h:
        with pytest.raises(error):
            xc.claim_ticket(12, "token", h)


def test_finalizacao_sem_solucao_e_status_invalido_nao_enviam(monkeypatch):
    monkeypatch.setenv(xc.BASE_URL_ENV, "https://x.test")
    with httpx.Client(transport=httpx.MockTransport(lambda req: pytest.fail("Envio inválido"))) as h:
        with pytest.raises(ValueError, match="solução"):
            xc.update_ticket(12, "Resolvido", " ", "token", h)
        with pytest.raises(ValueError, match="status"):
            xc.update_ticket(12, "Inventado", "", "token", h)


def test_fluxo_completo_estado_e_http_com_persistencia_simulada(state, monkeypatch):
    """Integra eventos reais ao cliente HTTP, sem credenciais/dados remotos."""
    monkeypatch.setenv(xc.BASE_URL_ENV, "https://simulado.test")
    stored = ticket(assigned=False)
    comments = []

    def api(req):
        assert req.headers["Authorization"] == "Bearer test-token"
        path = req.url.path
        if path == "/auth/me":
            return httpx.Response(200, json={"id": 30, "perfil_id": 3})
        if path == "/chamado":
            return httpx.Response(200, json=[stored])
        if path == "/chamado/12/assumir":
            assert stored["status_name"] == "Aberto"
            stored["tecnicos"].append({"id": 30, "name": "Técnico"})
            return httpx.Response(200, json={"id": 12})
        if path == "/interacao_chamado":
            if req.method == "POST":
                payload = json.loads(req.content)
                assert set(payload) == {"chamado_id", "mensagem"}
                comments.append({**payload, "id": 1, "user_id": 30, "author_name": "Técnico", "created_at": 1720000000000})
                return httpx.Response(200, json=comments[-1])
            assert req.url.params["chamado_id"] == "12"
            return httpx.Response(200, json=comments)
        assert path == "/chamado/12"
        if req.method == "PATCH":
            payload = json.loads(req.content)
            stored["status_name"] = payload["status_nome"]
            if payload.get("solucao_final"):
                stored["solucao_final"] = payload["solucao_final"]
        return httpx.Response(200, json=stored)

    with httpx.Client(transport=httpx.MockTransport(api)) as http:
        original = xc._request

        def request(*args, **kwargs):
            kwargs["client"] = http
            return original(*args, **kwargs)

        monkeypatch.setattr(xc, "_request", request)
        list(AuthState.verificar_sessao.fn(state))
        assert state.chamados_tecnicos
        list(AuthState.abrir_atendimento.fn(state, "12"))
        assert not state.tecnico_associado
        list(AuthState.executar_atendimento.fn(state, "associar"))
        assert state.tecnico_associado
        assert len(state.tecnicos_atendimento) == 2
        state.comentario = "Investigando impressão"
        list(AuthState.executar_atendimento.fn(state, "comentar"))
        assert state.historico[0]["mensagem"] == "Investigando impressão"
        assert state.comentario == ""
        state.status_destino = "Em atendimento"
        list(AuthState.executar_atendimento.fn(state, "status"))
        assert state.atendimento["status_name"] == "Em atendimento"
        state.status_destino = "Resolvido"
        state.solucao = "Fila de impressão corrigida"
        list(AuthState.executar_atendimento.fn(state, "status"))
        list(AuthState.abrir_atendimento.fn(state, "12"))
        assert state.atendimento["status_name"] == "Resolvido"
        assert state.atendimento["solucao_final"] == "Fila de impressão corrigida"
        assert not state.pode_atualizar_atendimento
