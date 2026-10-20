import csv
import io
import json

import pytest
import reflex as rx
import httpx

from TI_da_Firma import xano_client as api
from TI_da_Firma.admin_state import AdminState, history_csv
from TI_da_Firma.auth_state import AuthState
from TI_da_Firma.office_state import option_rows
from test_manager_portal import run


def session(profile=1):
    root = rx.State(_reflex_internal_init=True)
    auth = root.get_substate(AuthState._get_substate_path())
    admin = root.get_substate(AdminState._get_substate_path())
    auth.autenticado = True
    auth.auth_token = "test-token"
    auth.perfil_json = json.dumps({"id": 10, "perfil_id": profile, "departamento_id": 7})
    return auth, admin


def test_initialize_dashboard(monkeypatch):
    _, s = session()
    expected = {"abertos": 1, "em_andamento": 3, "finalizados": 2, "nao_classificados": 0, "total": 6}
    monkeypatch.setattr(api, "admin_metrics", lambda token: expected)
    run(AdminState.initialize, s)
    assert s.metrics == expected and s.section == "dashboard" and not s.loading


@pytest.mark.parametrize("profile", [2, 3, 4])
def test_non_admin_events_denied(monkeypatch, profile):
    _, s = session(profile)
    calls = []
    monkeypatch.setattr(api, "admin_metrics", lambda token: calls.append(token))
    run(AdminState.navigate, s, "dashboard")
    assert not calls and not s.metrics and s.error


def test_logout_and_restore_clear_admin():
    auth, s = session()
    s.metrics = {"total": 30}
    s.history = [{"mensagem": "private"}]
    s.ticket = {"id": "1"}
    auth._limpar_sessao()
    assert not s.metrics and not s.history and not s.ticket


def test_dashboard_failure_does_not_show_zero(monkeypatch):
    _, s = session()
    def fail(token):
        raise api.XanoUnavailable("failure")
    monkeypatch.setattr(api, "admin_metrics", fail)
    run(AdminState.navigate, s, "dashboard")
    assert s.error and not s.metrics and not s.loading


@pytest.mark.parametrize("profile", [1, 2, 3, 4])
def test_admin_provisions_each_role(monkeypatch, profile):
    _, s = session()
    s.profile_options = option_rows([{"id": profile, "name": "Perfil"}], "name")
    s.department_options = option_rows([{"id": 7, "nome": "RH"}])
    s.selected_profile = s.profile_labels[0]
    calls = []
    monkeypatch.setattr(api, "provision_user", lambda *args: calls.append(args) or {"id": 55})
    run(AdminState.create_user, s, {"name": "Ana", "email": "ana@test", "password": "Secret123", "departamento": s.department_labels[0]})
    assert calls[0][-2:] == (profile, 1 if profile == 3 else 7)
    assert s.success and not s.saving and "Secret123" not in str(s.dict())


def test_duplicate_submission_blocked(monkeypatch):
    _, s = session()
    s.saving = True
    monkeypatch.setattr(api, "provision_user", lambda *args: pytest.fail("duplicate write"))
    assert not run(AdminState.create_user, s, {})


def test_user_failure_preserves_form_revision_and_clears_password(monkeypatch):
    _, s = session()
    s.profile_options = option_rows([{"id": 4, "name": "Funcionário"}], "name")
    s.department_options = option_rows([{"id": 7, "nome": "RH"}])
    s.selected_profile = s.profile_labels[0]
    def fail(*args):
        raise api.XanoOperationError("Cadastro rejeitado")
    monkeypatch.setattr(api, "provision_user", fail)
    events = run(AdminState.create_user, s, {"departamento": s.department_labels[0], "password": "Secret123"})
    assert s.error and not s.success and s.form_revision == 0
    assert events[-1] is not None and "Secret123" not in str(s.dict())


def test_global_tasks_and_read_only_detail(monkeypatch):
    _, s = session()
    row = {"id": 9, "titulo": "Shared", "solicitante_id": 20, "requester_name": "Gestor", "responsaveis_ids": [30, 31],
           "responsaveis": [{"id": 30, "name": "A"}, {"id": 31, "name": "B"}], "concluido_em": "2026-10-20", "solucao_aplicada": "Done"}
    monkeypatch.setattr(api, "list_tasks", lambda token: [row])
    monkeypatch.setattr(api, "get_task", lambda token, task_id: row)
    monkeypatch.setattr(api, "complete_task", lambda *args: pytest.fail("read must not write"))
    run(AdminState.navigate, s, "tarefas")
    assert len(s.tasks) == 1 and s.tasks[0]["member_names"] == "A, B"
    run(AdminState.view_record, s, "tarefa", "9")
    assert s.task["solucao_aplicada"] == "Done" and s.task["requester_name"] == "Gestor"


def test_history_filter_and_pagination(monkeypatch):
    _, s = session()
    s.section = "logs"
    calls = []
    def history(token, ticket, page, boundary):
        calls.append((ticket, page, boundary))
        return {"items": [{"id": page, "chamado_id": 9, "mensagem": "Olá"}], "through_id": 50,
                "nextPage": 2 if page == 1 else None, "itemsTotal": 2}
    monkeypatch.setattr(api, "admin_history", history)
    run(AdminState.filter_history, s, {"chamado_id": "9"})
    run(AdminState.history_page, s, 2)
    assert calls == [(9, 1, None), (9, 2, 50)]
    assert s.history_filter == "9" and s.history[0]["author_name"] == "Autor indisponível"


def test_export_failure_no_download(monkeypatch):
    _, s = session()
    s.section = "logs"
    def fail(*args):
        raise api.XanoUnavailable("partial")
    monkeypatch.setattr(api, "admin_history_all", fail)
    events = run(AdminState.export_history, s)
    assert s.error and not s.saving
    assert not any("download" in str(e) for e in events)


def test_export_same_filter_no_content_in_state(monkeypatch):
    _, s = session()
    s.section, s._history_ticket_id = "logs", 9
    calls = []
    monkeypatch.setattr(api, "admin_history_all", lambda token, ticket: calls.append(ticket) or [{"id": 1, "mensagem": "private-export"}])
    events = run(AdminState.export_history, s)
    assert calls == [9] and any("download" in str(e) for e in events)
    assert "private-export" not in str(s.dict()) and not s.saving


@pytest.mark.parametrize("text", ["=1+1", " +2", "-3", "@SUM(A1)", "\tvalue", "\rvalue", "\nvalue"])
def test_csv_neutralizes_formulas(text):
    rows = list(csv.reader(io.StringIO(history_csv([{"mensagem": text}]).decode("utf-8-sig"))))
    assert rows[1][-1] == "'" + text


def test_csv_unicode_quotes_newline_and_empty():
    text = 'Olá, "mundo"\nsegunda linha'
    data = history_csv([{"mensagem": text, "password": "secret"}])
    assert data.startswith(b"\xef\xbb\xbf") and b"secret" not in data
    assert list(csv.reader(io.StringIO(data.decode("utf-8-sig"))))[1][-1] == text
    assert len(list(csv.reader(io.StringIO(history_csv([]).decode("utf-8-sig"))))) == 1


def test_client_history_all_boundary_and_dedup(monkeypatch):
    calls = []
    def page(token, ticket, page, boundary):
        calls.append((ticket, page, boundary))
        return {"items": [{"id": 1}] if page == 1 else [{"id": 1}, {"id": 2}],
                "through_id": 2, "nextPage": 2 if page == 1 else None, "itemsTotal": 2}
    monkeypatch.setattr(api, "admin_history", page)
    assert api.admin_history_all("token", 9) == [{"id": 1}, {"id": 2}]
    assert calls == [(9, 1, None), (9, 2, 2)]


@pytest.mark.parametrize("next_page,total", [(1, 2), (None, 2)])
def test_client_detects_cycle_or_partial(monkeypatch, next_page, total):
    monkeypatch.setattr(api, "admin_history", lambda *args: {"items": [{"id": 1}], "through_id": 2, "nextPage": next_page, "itemsTotal": total})
    with pytest.raises(api.XanoUnavailable):
        api.admin_history_all("token")


@pytest.mark.parametrize("payload", [
    {"items": [{"id": 1, "chamado_id": 10}], "through_id": 2},
    {"items": [{"id": 3, "chamado_id": 9}], "through_id": 2},
    {"items": [], "through_id": 3},
    {"items": [], "through_id": 2, "nextPage": 1},
])
def test_client_rejects_invalid_history_scope(monkeypatch, payload):
    monkeypatch.setattr(api, "office_request", lambda *args, **kwargs: payload)
    with pytest.raises(api.XanoUnavailable):
        api.admin_history("token", 9, 1, 2)


def test_client_transport_and_metrics(monkeypatch):
    calls = []
    expected = {"abertos": 1, "em_andamento": 2, "finalizados": 3, "nao_classificados": 0, "total": 6}
    monkeypatch.setattr(api, "office_request", lambda *args, **kwargs: calls.append((args, kwargs)) or expected)
    assert api.admin_metrics("token") == expected
    assert calls[0][0] == ("GET", "helpdesk/metrics/tickets", "token")
    expected["total"] = 7
    with pytest.raises(api.XanoUnavailable):
        api.admin_metrics("token")


def test_rejected_session_clears_admin(monkeypatch):
    auth, s = session()
    s.history = [{"mensagem": "private"}]
    def reject(*args):
        raise api.XanoRejected("expired")
    monkeypatch.setattr(api, "admin_metrics", reject)
    run(AdminState.navigate, s, "dashboard")
    assert not auth.autenticado and not s.history and not s.metrics


def test_history_http_transport_and_token(monkeypatch):
    monkeypatch.setenv("XANO_API_BASE_URL", "https://example.test/api:test")
    requests = []
    def handle(request):
        requests.append(request)
        return httpx.Response(200, json={"items": [], "through_id": 0, "nextPage": None, "itemsTotal": 0})
    with httpx.Client(transport=httpx.MockTransport(handle)) as client:
        original = api.office_request
        monkeypatch.setattr(api, "office_request", lambda *args, **kwargs: original(*args, **kwargs, client=client))
        assert api.admin_history_all("test-token", 9) == []
    assert requests[0].headers["Authorization"] == "Bearer test-token"
    assert requests[0].url.path.endswith("/helpdesk/tickets/history")
    assert requests[0].url.params["chamado_id"] == "9"
    assert "test-token" not in str(requests[0].url)


def test_global_ticket_detail_is_read_only(monkeypatch):
    _, s = session()
    row = {"id": 55, "titulo": "External", "solicitante_id": 99, "requester_name": "Pessoa",
           "tecnicos": [{"id": 30, "name": "A"}, {"id": 31, "name": "B"}], "status_name": "Fechado"}
    monkeypatch.setattr(api, "technician_tickets", lambda token: [row])
    monkeypatch.setattr(api, "technician_ticket", lambda *args: row)
    monkeypatch.setattr(api, "update_ticket", lambda *args: pytest.fail("read must not write"))
    run(AdminState.navigate, s, "chamados")
    run(AdminState.view_record, s, "chamado", "55")
    assert s.ticket["status_name"] == "Fechado" and s.ticket["technician_names"] == "A, B"


def test_expired_export_clears_and_redirects(monkeypatch):
    auth, s = session()
    s.section = "logs"
    def reject(*args):
        raise api.XanoRejected("expired")
    monkeypatch.setattr(api, "admin_history_all", reject)
    events = run(AdminState.export_history, s)
    assert not auth.autenticado and not s.saving
    assert not any("download" in str(e) for e in events)
