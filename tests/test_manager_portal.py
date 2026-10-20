import asyncio
import json

import httpx
import pytest
import reflex as rx

from TI_da_Firma.auth_state import AuthState
from TI_da_Firma.office_state import OfficeState, option_rows
from TI_da_Firma import xano_client as api


def run(event, *args):
    async def collect():
        return [value async for value in event.fn(*args)]
    return asyncio.run(collect())


def session(profile=2, department=1):
    root = rx.State(_reflex_internal_init=True)
    auth = root.get_substate(AuthState._get_substate_path())
    office = root.get_substate(OfficeState._get_substate_path())
    auth.autenticado = True
    auth.auth_token = "test-token"
    auth.perfil_json = json.dumps({"id": 30, "perfil_id": profile, "departamento_id": department})
    office.manager = profile == 2
    office.ti_manager = profile == 2 and department == 1
    return auth, office


@pytest.mark.parametrize("department,profile", [(1, 3), (7, 4)])
def test_gestor_carrega_responsaveis_do_escopo_correto(monkeypatch, department, profile):
    _, s = session(department=department)
    calls = []
    monkeypatch.setattr(api, "list_priorities", lambda token: [{"id": 2, "nome": "Alta"}])
    monkeypatch.setattr(api, "directory", lambda token, p, d: calls.append((p, d)) or [{"id": 10, "name": "Pessoa"}])
    run(OfficeState.navigate, s, "nova_tarefa")
    assert calls == [(profile, department)]
    assert s.owner_labels == ["Pessoa (#10)"]
    assert not s.error and not s.loading


@pytest.mark.parametrize("department,expected", [(1, {2, 3, 4}), (7, {4})])
def test_perfis_de_cadastro_permitidos(monkeypatch, department, expected):
    _, s = session(department=department)
    monkeypatch.setattr(api, "departments", lambda token: [{"id": 1, "nome": "TI"}, {"id": 7, "nome": "RH"}])
    monkeypatch.setattr(api, "profiles", lambda token: [{"id": n, "name": str(n)} for n in range(1, 5)])
    run(OfficeState.navigate, s, "usuarios")
    assert {int(r["id"]) for r in s.profile_options} == expected
    assert {r["id"] for r in s.department_options} == ({"1", "7"} if department == 1 else {"7"})


def test_cadastro_tecnico_fixa_ti_sem_guardar_senha(monkeypatch):
    _, s = session()
    s.profile_options = option_rows([{"id": 3, "name": "Técnico"}], "name")
    s.selected_profile = s.profile_labels[0]
    calls = []
    monkeypatch.setattr(api, "provision_user", lambda *a: calls.append(a) or {"id": 5})
    events = run(OfficeState.submit, s, "usuario", {"name": "Ana", "email": "a@test", "password": "Teste123"})
    assert calls[0][-2:] == (3, 1)
    assert s.success and not s.saving
    assert "Teste123" not in str(s.dict())
    assert events[-1] is not None  # limpeza do campo de senha no navegador


def test_erro_usuario_nao_anuncia_sucesso_e_limpa_senha(monkeypatch):
    auth, s = session(department=7)
    s.profile_options = [{"id": "4", "label": "Funcionário"}]
    s.selected_profile = "Funcionário"
    s.department_options = [{"id": "7", "label": "RH"}]

    def reject(*a):
        raise api.XanoOperationError("Cadastro rejeitado")

    monkeypatch.setattr(api, "provision_user", reject)
    events = run(OfficeState.submit, s, "usuario", {"name": "Ana", "email": "a@test", "password": "Teste123", "departamento": "RH"})
    assert s.error == "Cadastro rejeitado" and not s.success
    assert auth.autenticado
    assert events[-1] is not None


def test_funcionario_nao_acessa_formularios_gerenciais(monkeypatch):
    _, s = session(profile=4, department=7)
    monkeypatch.setattr(api, "provision_user", lambda *a: pytest.fail("Acesso indevido"))
    run(OfficeState.submit, s, "usuario", {})
    assert s.error and not s.success


@pytest.mark.parametrize("profile", [3, 4])
def test_tarefa_propria_conclui_com_solucao_e_nao_chama_api_chamado(monkeypatch, profile):
    _, s = session(profile=profile, department=7)
    s.task = {"id": "12", "responsavel_id": "30"}
    s.solution = "Trabalho concluído"
    calls = []
    monkeypatch.setattr(api, "complete_task", lambda *a: calls.append(a) or {
        "id": 12, "responsavel_id": 30, "concluido_em": "2026-10-20", "solucao_aplicada": "Trabalho concluído"})
    monkeypatch.setattr(api, "update_ticket", lambda *a: pytest.fail("Chamado não pode ser alterado"))
    run(OfficeState.submit, s, "concluir", {})
    assert calls == [("test-token", 12, "Trabalho concluído")]
    assert s.task["status_nome"] == "Concluída" and s.success


@pytest.mark.parametrize("profile", [3, 4])
def test_tarefa_alheia_rejeitada_no_detalhe_e_conclusao(monkeypatch, profile):
    _, s = session(profile=profile)
    monkeypatch.setattr(api, "get_task", lambda *a: {"id": 12, "responsavel_id": 99})
    run(OfficeState.view_task, s, "12")
    assert not s.task and s.error
    s.task = {"id": "12", "responsavel_id": "99"}
    monkeypatch.setattr(api, "complete_task", lambda *a: pytest.fail("Tarefa alheia"))
    run(OfficeState.submit, s, "concluir", {})
    assert s.error and not s.success


@pytest.mark.parametrize("profile", [3, 4])
def test_lista_tarefas_ignora_resposta_sem_escopo(monkeypatch, profile):
    _, s = session(profile=profile)
    monkeypatch.setattr(api, "list_tasks", lambda *a: [{"id": 1, "responsavel_id": 99}])
    run(OfficeState.navigate, s, "tarefas")
    assert s.error and not s.tasks


def test_falha_conclusao_preserva_solucao_e_nao_sucesso(monkeypatch):
    auth, s = session(profile=4)
    s.task = {"id": "12", "responsavel_id": "30"}
    s.solution = "Meu rascunho"

    def fail(*a):
        raise api.XanoUnavailable()

    monkeypatch.setattr(api, "complete_task", fail)
    run(OfficeState.submit, s, "concluir", {})
    assert s.solution == "Meu rascunho" and s.error and not s.success and auth.autenticado


def test_logout_e_restauracao_limpam_estado_gerencial():
    auth, s = session()
    s.ticket = {"id": "12", "descricao": "Privado"}
    s.solution = "Rascunho"
    AuthState.sair.fn(auth)
    assert not s.ticket and not s.solution and not auth.autenticado


def test_rejeicao_sessao_limpa_tarefas(monkeypatch):
    auth, s = session(profile=4)
    s.tasks = [{"id": "12"}]

    def expired(*a):
        raise api.XanoRejected()

    monkeypatch.setattr(api, "list_tasks", expired)
    run(OfficeState.navigate, s, "tarefas")
    assert not s.tasks and not auth.autenticado and not auth.auth_token


def test_envio_duplo_nao_grava(monkeypatch):
    _, s = session()
    s.saving = True
    monkeypatch.setattr(api, "create_task", lambda *a: pytest.fail("Envio duplicado"))
    run(OfficeState.submit, s, "tarefa", {})
    assert s.saving


@pytest.mark.parametrize("profile", [3, 4])
def test_inicio_trabalhador_carrega_tarefas_e_limpa_rascunho(monkeypatch, profile):
    _, s = session(profile=profile, department=7)
    s.solution = "Anterior"
    monkeypatch.setattr(api, "list_tasks", lambda token: [{"id": 12, "responsavel_id": 30, "titulo": "Conferir estoque"}])
    run(OfficeState.initialize, s)
    assert s.section == "tarefas" and s.tasks[0]["id"] == "12"
    assert s.solution == "" and not s.manager and not s.loading


def test_diretorio_busca_todas_as_paginas(monkeypatch):
    calls = []

    def request(method, path, token, *, params):
        calls.append(params["page"])
        return {"items": [{"id": params["page"], "perfil_id": 4, "departamento_id": 7}],
                "nextPage": 2 if params["page"] == 1 else None}

    monkeypatch.setattr(api, "office_request", request)
    assert len(api.directory("token", 4, 7)) == 2
    assert calls == [1, 2]


def test_diretorio_rejeita_paginacao_circular(monkeypatch):
    monkeypatch.setattr(api, "office_request", lambda *a, **kw: {"items": [], "nextPage": 1})
    with pytest.raises(api.XanoUnavailable, match="Paginação"):
        api.directory("token", 4, 7)


def test_contratos_de_gravacao_nao_enviam_autoria_status_indevidos(monkeypatch):
    calls = []
    monkeypatch.setattr(api, "office_request", lambda *a, **kw: calls.append((a, kw)) or {"id": 1})
    api.create_task("token", "Título", "Texto", 40, 2)
    assert calls[-1][1]["payload"] == {"titulo": "Título", "descricao": "Texto", "responsavel_id": 40, "prioridade_id": 2}
    api.complete_task("token", 1, " Feito ")
    assert calls[-1][1]["payload"] == {"status_nome": "Concluída", "solucao_aplicada": "Feito"}
    with pytest.raises(ValueError):
        api.complete_task("token", 1, " ")
