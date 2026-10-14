"""Testes locais das mensagens e decisões do carregamento dos catálogos."""

import pytest

from TI_da_Firma.ticket_state import _missing_options_message, _options_rejection


@pytest.mark.parametrize(
    ("status_code", "should_clear_session"),
    [(401, True), (403, False), (400, False)],
)
def test_rejeicao_do_catalogo_so_limpa_sessao_em_401(
    status_code, should_clear_session
):
    clear_session, message = _options_rejection(status_code)

    assert clear_session is should_clear_session
    assert message


def test_catalogos_vazios_sao_reportados_separadamente():
    assert "categorias nem prioridades" in _missing_options_message([], [])
    assert "Não há categorias" in _missing_options_message([], [{"id": 1}])
    assert "Não há prioridades" in _missing_options_message([{"id": 1}], [])
    assert _missing_options_message([{"id": 1}], [{"id": 1}]) == ""