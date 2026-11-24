import json

import httpx
import pytest
import reflex as rx

from TI_da_Firma import xano_client as api
from TI_da_Firma.auth_state import AuthState
from TI_da_Firma.admin_state import AdminState
from TI_da_Firma.office_state import OfficeState
from TI_da_Firma.ticket_filters import TicketFilters
from test_manager_portal import run


def filter_session(role=4):
    root = rx.State(_reflex_internal_init=True)
    auth = root.get_substate(AuthState._get_substate_path())
    filters = root.get_substate(TicketFilters._get_substate_path())
    auth.autenticado = True
    auth.auth_token = "test-token"
    auth.perfil_json = json.dumps({"id": 10, "perfil_id": role, "departamento_id": 7})
    return root, auth, filters


def test_combined_filter_transport(monkeypatch):
    monkeypatch.setenv("XANO_API_BASE_URL", "https://example.test/api:test")
    requests = []
    def handle(request):
        requests.append(request)
        return httpx.Response(200, json=[{"id": 1, "prioridade_id": 8, "status_chamado_id": 9,
                                        "requester_name": "Marina Costa"}])
    with httpx.Client(transport=httpx.MockTransport(handle)) as client:
        assert len(api.search_tickets("secret", 8, 9, "  MARINA  ", client)) == 1
    assert dict(requests[0].url.params) == {"prioridade_id": "8", "status_chamado_id": "9", "solicitante_nome": "MARINA"}
    assert requests[0].headers["Authorization"] == "Bearer secret"
    assert "secret" not in str(requests[0].url)


@pytest.mark.parametrize("row", [{"prioridade_id": 2}, {"prioridade_id": 1, "status_chamado_id": 3},
                                    {"prioridade_id": 1, "status_chamado_id": 2, "requester_name": "Outra pessoa"}])
def test_fail_if_old_backend_ignores_filters(monkeypatch, row):
    monkeypatch.setattr(api, "_request", lambda *a, **kw: [row])
    with pytest.raises(api.XanoUnavailable):
        api.search_tickets("token", 1, 2, "Marina")


@pytest.mark.parametrize("priority,status,name", [(0, None, ""), (None, -1, ""), (True, None, ""), (None, None, "a" * 201)])
def test_invalid_filters_never_make_request(monkeypatch, priority, status, name):
    monkeypatch.setattr(api, "_request", lambda *a, **kw: pytest.fail("invalid request"))
    with pytest.raises(ValueError):
        api.search_tickets("token", priority, status, name)


@pytest.mark.parametrize("role", [1, 2, 3, 4])
def test_apply_and_clear_by_role(monkeypatch, role):
    root, auth, filters = filter_session(role)
    filters.priorities = [{"id": "8", "label": "Alta (#8)"}]
    filters.statuses = [{"id": "9", "label": "Aberto (#9)"}]
    filters.priority, filters.status, filters.requester = "Alta (#8)", "Aberto (#9)", "Marina"
    calls = []
    def search(*args):
        calls.append(args)
        return [{"id": 1, "titulo": "Impressora", "solicitante_id": 10}]
    monkeypatch.setattr(api, "search_tickets", search)
    run(TicketFilters.apply, filters, False)
    assert calls[0] == ("test-token", 8, 9, "Marina")
    if role == 1:
        rows = root.get_substate(AdminState._get_substate_path()).tickets
    elif role == 2:
        rows = root.get_substate(OfficeState._get_substate_path()).tickets
    else:
        rows = auth.chamados_tecnicos if role == 3 else auth.chamados
    assert len(rows) == 1 and rows[0]["id"] == "1"
    run(TicketFilters.apply, filters, True)
    assert calls[-1] == ("test-token", None, None, "")


def test_employee_foreign_records_fail_closed(monkeypatch):
    _, auth, filters = filter_session()
    monkeypatch.setattr(api, "search_tickets", lambda *a: [{"id": 1, "solicitante_id": 99}])
    run(TicketFilters.apply, filters, False)
    assert not auth.chamados and filters.error


def test_expiration_clears_all_filter_state(monkeypatch):
    _, auth, filters = filter_session()
    filters.requester = "Marina"
    def reject(*a):
        raise api.XanoRejected("expired")
    monkeypatch.setattr(api, "search_tickets", reject)
    run(TicketFilters.apply, filters, False)
    assert not auth.autenticado and not filters.requester and not auth.chamados


def test_empty_and_error_are_distinct(monkeypatch):
    _, _, filters = filter_session()
    monkeypatch.setattr(api, "search_tickets", lambda *a: [])
    run(TicketFilters.apply, filters, False)
    assert filters.error == ""
    def failure(*a):
        raise api.XanoUnavailable("network")
    monkeypatch.setattr(api, "search_tickets", failure)
    run(TicketFilters.apply, filters, False)
    assert filters.error and not filters.loading


def test_switch_from_open_to_resolved_and_clear(monkeypatch):
    _, auth, filters = filter_session()
    rows = [
        {"id": 1, "status_chamado_id": 8, "status_name": "Aberto", "solicitante_id": 10},
        {"id": 2, "status_chamado_id": 9, "status_name": "Resolvido", "solicitante_id": 10},
    ]
    filters.statuses = [{"id": "8", "label": "Aberto (#8)"}, {"id": "9", "label": "Resolvido (#9)"}]

    def request(*args, params, **kwargs):
        status = params.get("status_chamado_id")
        return [row for row in rows if status is None or row["status_chamado_id"] == status]

    monkeypatch.setattr(api, "_request", request)
    for label, expected in (("Aberto (#8)", "Aberto"), ("Resolvido (#9)", "Resolvido")):
        TicketFilters.set_status.fn(filters, label)
        run(TicketFilters.apply, filters, False)
        assert [row["status_name"] for row in auth.lista_visual_chamados] == [expected]

    run(TicketFilters.apply, filters, True)
    assert [row["status_name"] for row in auth.lista_visual_chamados] == ["Aberto", "Resolvido"]


def test_status_mismatch_is_reported_in_the_search_panel(monkeypatch):
    _, _, filters = filter_session()
    filters.statuses = [{"id": "9", "label": "Resolvido (#9)"}]
    filters.status = "Resolvido (#9)"
    monkeypatch.setattr(api, "_request", lambda *args, **kwargs: [{"status_chamado_id": 8}])

    run(TicketFilters.apply, filters, False)

    assert filters.error == "O Xano devolveu chamados que não correspondem aos filtros selecionados."
