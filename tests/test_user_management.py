import httpx
import pytest

from TI_da_Firma import xano_client as api
from TI_da_Firma.admin_state import AdminState
from TI_da_Firma.office_state import option_rows
from test_admin_portal import session
from test_manager_portal import run


def test_admin_directory_global_transport_and_secret_projection(monkeypatch):
    monkeypatch.setenv("XANO_API_BASE_URL", "https://example.test/api:test")
    requests = []

    def handle(request):
        requests.append(request)
        return httpx.Response(200, json={"curPage": 2, "nextPage": 3, "itemsTotal": 110,
            "items": [{"id": 51, "name": "Pessoa", "email": "p@example.test", "perfil_id": 1,
                       "departamento_id": None, "status": "Inativo", "password": "secret", "password_reset": {"token": "secret"}}]})

    original = api.office_request
    with httpx.Client(transport=httpx.MockTransport(handle)) as client:
        monkeypatch.setattr(api, "office_request", lambda *a, **kw: original(*a, **kw, client=client))
        data = api.admin_users("token", 2)
    assert data["next_page"] == 3 and data["total"] == 110
    assert set(data["items"][0]) == set(api.ADMIN_USER_FIELDS)
    assert "perfil_id" not in requests[0].url.params and "departamento_id" not in requests[0].url.params
    assert requests[0].headers["Authorization"] == "Bearer token"


@pytest.mark.parametrize("change", [{"nextPage": 1}, {"curPage": 2}, {"itemsTotal": -1}, {"nextPage": "2"}])
def test_reject_invalid_directory_pagination(monkeypatch, change):
    data = {"curPage": 1, "items": [], "nextPage": None, "itemsTotal": 0, **change}
    monkeypatch.setattr(api, "office_request", lambda *a, **kw: data)
    with pytest.raises(api.XanoUnavailable):
        api.admin_users("token")


@pytest.mark.parametrize("status", [401, 403])
def test_directory_rejection_propagates(monkeypatch, status):
    monkeypatch.setenv("XANO_API_BASE_URL", "https://example.test/api:test")
    original = api.office_request
    with httpx.Client(transport=httpx.MockTransport(lambda r: httpx.Response(status))) as client:
        monkeypatch.setattr(api, "office_request", lambda *a, **kw: original(*a, **kw, client=client))
        with pytest.raises((api.XanoRejected, api.XanoOperationError)):
            api.admin_users("token")


@pytest.mark.parametrize("fields", [{"id": 4}, {"password": "secret"}, {"password_reset": {}},
                                      {"status": "Outro"}, {"perfil_id": True}, {"departamento_id": -1}])
def test_edit_rejects_immutable_and_invalid_fields(monkeypatch, fields):
    monkeypatch.setattr(api, "office_request", lambda *a, **kw: pytest.fail("request must not be sent"))
    with pytest.raises(ValueError):
        api.edit_user("token", 2, fields)


def test_detail_and_update_verify_identity(monkeypatch):
    monkeypatch.setattr(api, "office_request", lambda *a, **kw: {"id": 99})
    with pytest.raises(api.XanoUnavailable):
        api.admin_user("token", 1)
    with pytest.raises(api.XanoUnavailable):
        api.edit_user("token", 1, {"name": "Pessoa"})


def test_user_list_page_and_logout_isolation(monkeypatch):
    auth, state = session()
    state.section = "usuarios"
    monkeypatch.setattr(api, "admin_users", lambda token, page: {
        "items": [{"id": 51, "name": "Pessoa", "email": "p@test"}], "next_page": 3, "total": 120})
    run(AdminState.users_page_at, state, 2)
    assert state.users_page == 2 and state.users_next_page == 3
    assert state.users[0]["id"] == "51"
    auth._limpar_sessao()
    assert not state.users and not state.user and state.users_page == 1


@pytest.mark.parametrize("role", [2, 3, 4])
def test_user_management_rejects_non_admin_state(monkeypatch, role):
    _, state = session(role)
    state.section = "usuarios"
    monkeypatch.setattr(api, "admin_users", lambda *a: pytest.fail("unauthorized"))
    run(AdminState.users_page_at, state, 1)
    assert state.error and not state.users


def test_save_user_preserves_draft_on_rejection(monkeypatch):
    _, state = session()
    state.section, state.user_mode = "usuarios", "edit"
    state.user = {"id": "5", "name": "Anterior"}
    state.profile_options = option_rows([{"id": 4, "name": "Funcionário"}], "name")
    state.department_options = option_rows([{"id": 7, "nome": "RH"}])
    state.selected_profile = state.profile_labels[0]
    def reject(*a):
        raise api.XanoOperationError("E-mail duplicado")
    monkeypatch.setattr(api, "edit_user", reject)
    run(AdminState.save_user, state, {"name": "Pessoa", "email": "p@test", "status": "Ativo",
                                    "departamento": state.department_labels[0]})
    assert state.error and not state.success and state.user_mode == "edit"
    assert state.form_revision == 0 and not state.saving


def test_save_user_refreshes_list_without_credentials(monkeypatch):
    _, state = session()
    state.section, state.user_mode = "usuarios", "edit"
    state.user = {"id": "5", "name": "Antes"}
    state.profile_options = option_rows([{"id": 4, "name": "Funcionário"}], "name")
    state.department_options = option_rows([{"id": 7, "nome": "RH"}])
    state.selected_profile = state.profile_labels[0]
    saved = {}
    def edit(token, user_id, fields):
        saved.update({"id": user_id, **fields})
        return saved
    monkeypatch.setattr(api, "edit_user", edit)
    monkeypatch.setattr(api, "admin_users", lambda *a: {"items": [saved], "next_page": 0, "total": 1})
    run(AdminState.save_user, state, {"name": "Depois", "email": "p@test", "status": "Inativo",
                                    "departamento": state.department_labels[0], "password": "never forward"})
    assert state.users[0]["name"] == "Depois" and state.users[0]["status"] == "Inativo"
    assert state.success and state.user_mode == "list" and not state.saving
    assert "password" not in saved


def test_save_user_duplicate_submission_makes_no_request(monkeypatch):
    _, state = session()
    state.section, state.user_mode, state.saving = "usuarios", "edit", True
    monkeypatch.setattr(api, "edit_user", lambda *a: pytest.fail("duplicate write"))
    run(AdminState.save_user, state, {})


def test_manual_password_creation_remains_one_authenticated_request(monkeypatch):
    monkeypatch.setenv("XANO_API_BASE_URL", "https://example.test/api:test")
    requests = []
    def handle(request):
        requests.append(request)
        assert request.method == "POST" and request.url.path.endswith("/users/create")
        assert request.headers["Authorization"] == "Bearer token"
        import json
        assert json.loads(request.content)["password"] == "Manual123"
        return httpx.Response(200, json={"id": 5, "name": "Pessoa"})
    original = api.office_request
    with httpx.Client(transport=httpx.MockTransport(handle)) as client:
        monkeypatch.setattr(api, "office_request", lambda *a, **kw: original(*a, **kw, client=client))
        result = api.provision_user("token", "Pessoa", "p@test", "Manual123", 4, 7)
    assert result["id"] == 5 and "password" not in result and len(requests) == 1
