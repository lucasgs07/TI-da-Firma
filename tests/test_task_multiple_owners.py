import pytest

from TI_da_Firma import xano_client as api
from TI_da_Firma.office_state import OfficeState, public_task, task_member_ids
from test_manager_portal import run, session


@pytest.mark.parametrize("profile", [3, 4])
def test_second_owner_can_list_open_and_complete_global_task(monkeypatch, profile):
    _, state = session(profile=profile, department=1 if profile == 3 else 7)
    record = {"id": 12, "titulo": "Tarefa conjunta", "responsavel_id": 31,
              "responsaveis_ids": [31, 30], "responsaveis": [{"id": 31, "name": "Ana"}, {"id": 30, "name": "Beto"}]}
    monkeypatch.setattr(api, "list_tasks", lambda *args: [record.copy()])
    monkeypatch.setattr(api, "get_task", lambda *args: record.copy())

    def complete(token, task_id, solution):
        record.update(solucao_aplicada=solution, concluido_em="2026-10-20")
        return record.copy()

    monkeypatch.setattr(api, "complete_task", complete)
    run(OfficeState.navigate, state, "tarefas")
    assert len(state.tasks) == 1
    run(OfficeState.view_task, state, "12")
    assert state.task["member_names"] == "Ana, Beto"
    state.solution = "Solução global"
    run(OfficeState.submit, state, "concluir", {})
    assert not state.error and state.task["status_nome"] == "Concluída"
    # Any other associated person gets the same global state on a new read.
    assert api.get_task("other-token", 12)["solucao_aplicada"] == "Solução global"
    assert api.get_task("other-token", 12)["concluido_em"] == "2026-10-20"


def test_authoritative_list_does_not_grant_access_via_stale_primary(monkeypatch):
    _, state = session(profile=3)
    record = {"id": 12, "responsavel_id": 30, "responsaveis_ids": [31, 32]}
    monkeypatch.setattr(api, "get_task", lambda *args: record)
    run(OfficeState.view_task, state, "12")
    assert state.error and not state.task
    assert task_member_ids(record) == ["31", "32"]


@pytest.mark.parametrize("owners", [None, []])
def test_legacy_task_remains_visible(owners):
    record = {"id": 12, "responsavel_id": 30, "responsaveis_ids": owners}
    assert task_member_ids(record) == ["30"]
    assert public_task(record)["member_ids"] == "30"


def test_multi_create_sends_deduplicated_array_without_legacy_field(monkeypatch):
    captured = []
    monkeypatch.setattr(api, "office_request", lambda *a, **kw: captured.append(kw["payload"]) or {"id": 1})
    api.create_task("token", "Título", "Descrição", [31, 30, 31], 2)
    assert captured[0]["responsaveis_ids"] == [31, 30]
    assert "responsavel_id" not in captured[0]


@pytest.mark.parametrize("owners", [[], [0], [-1], ["30"], [True]])
def test_invalid_multi_selection_never_sends_request(monkeypatch, owners):
    monkeypatch.setattr(api, "office_request", lambda *a, **kw: pytest.fail("Invalid owner list was sent"))
    with pytest.raises(ValueError):
        api.create_task("token", "Título", "", owners, 2)


@pytest.mark.parametrize("department", [1, 7])
def test_manager_submits_every_checked_owner(monkeypatch, department):
    _, state = session(department=department)
    state.owner_options = [{"id": "31", "label": "Ana"}, {"id": "32", "label": "Beto"}]
    state.priority_options = [{"id": "2", "label": "Alta"}]
    OfficeState.toggle_owner.fn(state, "Ana", True)
    OfficeState.toggle_owner.fn(state, "Beto", True)
    OfficeState.toggle_owner.fn(state, "Ana", True)
    assert state.selected_owners == ["Ana", "Beto"]
    captured = []
    monkeypatch.setattr(api, "create_task", lambda *args: captured.append(args) or {"id": 12})
    run(OfficeState.submit, state, "tarefa", {"titulo": "Tarefa conjunta", "prioridade": "Alta"})
    assert captured[0][3] == [31, 32]
    assert state.success and not state.selected_owners


def test_empty_selection_preserves_form_and_does_not_create(monkeypatch):
    _, state = session()
    monkeypatch.setattr(api, "create_task", lambda *args: pytest.fail("No responsible user selected"))
    run(OfficeState.submit, state, "tarefa", {"titulo": "Tarefa conjunta"})
    assert state.error and not state.success


def test_failed_creation_preserves_all_selected_owners(monkeypatch):
    _, state = session()
    state.owner_options = [{"id": "31", "label": "Ana"}, {"id": "32", "label": "Beto"}]
    state.selected_owners = ["Ana", "Beto"]
    state.priority_options = [{"id": "2", "label": "Alta"}]

    def reject(*args):
        raise api.XanoOperationError("Responsible user no longer eligible")

    monkeypatch.setattr(api, "create_task", reject)
    run(OfficeState.submit, state, "tarefa", {"titulo": "Tarefa conjunta", "prioridade": "Alta"})
    assert state.selected_owners == ["Ana", "Beto"] and state.error and not state.success
