"""Estado de autenticação: login, restauração de sessão e logout local."""

import json

import reflex as rx

from . import xano_client

PERFIS = {1: "Administrador", 2: "Gestor", 3: "Técnico", 4: "Funcionário"}


def _rota_pos_login(perfil_id: object) -> str:
    return "/chamados/novo" if str(perfil_id) == "4" else "/"


class AuthState(rx.State):
    # Persistidos no LocalStorage do navegador (sobrevivem ao fechar o navegador).
    auth_token: str = rx.LocalStorage("", name="auth_token")
    perfil_json: str = rx.LocalStorage("", name="auth_perfil")

    # Estado efêmero de interface.
    autenticado: bool = False
    carregando: bool = False
    erro: str = ""
    erro_rede: bool = False

    @rx.var
    def perfil(self) -> dict[str, str]:
        try:
            data = json.loads(self.perfil_json) if self.perfil_json else {}
        except ValueError:
            data = {}
        return {k: "" if v is None else str(v) for k, v in data.items()}

    @rx.var
    def nome_perfil(self) -> str:
        try:
            return PERFIS.get(int(self.perfil.get("perfil_id", "")), "Desconhecido")
        except ValueError:
            return "Desconhecido"

    @rx.var
    def pode_criar_chamado(self) -> bool:
        try:
            return int(self.perfil.get("perfil_id", "")) in (2, 4)
        except ValueError:
            return False

    def _salvar_perfil(self, user: dict) -> None:
        self.perfil_json = json.dumps(user)

    def _limpar_sessao(self) -> None:
        self.auth_token = ""
        self.perfil_json = ""
        self.autenticado = False

    def get_auth_headers(self) -> dict[str, str]:
        """Cabeçalho para futuras chamadas autenticadas ao Xano."""
        return xano_client.auth_headers(self.auth_token)

    @rx.event
    def entrar(self, form_data: dict):
        email = str(form_data.get("email", "")).strip()
        senha = str(form_data.get("password", ""))
        self.erro = ""
        self.erro_rede = False
        if not email or not senha:
            self.erro = "Informe e-mail e senha."
            return
        self.carregando = True
        yield
        try:
            resultado = xano_client.login(email, senha)
        except xano_client.XanoConfigError as exc:
            self.erro = str(exc)
        except xano_client.XanoRejected as exc:
            if exc.status_code == 403:
                self.erro = (
                    "O Xano recusou o login. Confira e-mail e senha; se estiverem "
                    "corretos, valide se a conta tem perfil operacional e departamento configurados."
                )
            elif exc.status_code == 401:
                self.erro = "O Xano recusou as credenciais informadas."
            else:
                self.erro = "O Xano rejeitou os dados do login. Confira o formato do e-mail."
        except xano_client.XanoUnavailable:
            self.erro = "Não foi possível conectar ao servidor. Tente novamente."
        else:
            self.auth_token = resultado.auth_token
            self._salvar_perfil(resultado.user)
            self.autenticado = True
            self.carregando = False
            return rx.redirect(_rota_pos_login(resultado.user.get("perfil_id")))
        self.carregando = False

    @rx.event
    def verificar_sessao(self):
        """Guarda da página protegida: valida o token com auth/me."""
        self.erro = ""
        self.erro_rede = False
        self.autenticado = False
        if not self.auth_token:
            return rx.redirect("/login")
        self.carregando = True
        yield
        try:
            user = xano_client.me(self.auth_token)
        except xano_client.XanoRejected:
            self._limpar_sessao()
            self.carregando = False
            return rx.redirect("/login")
        except xano_client.XanoConfigError as exc:
            self.erro = str(exc)
            self.erro_rede = True
        except xano_client.XanoUnavailable:
            self.erro = "Não foi possível validar a sessão. Verifique a conexão."
            self.erro_rede = True
        else:
            self._salvar_perfil(user)
            self.autenticado = True
        self.carregando = False

    @rx.event
    def verificar_login(self):
        """Na tela de login, quem tem token segue à rota adequada ao perfil."""
        if self.auth_token:
            return rx.redirect(_rota_pos_login(self.perfil.get("perfil_id", "")))

    @rx.event
    def sair(self):
        """Logout local: o token no Xano continua válido até expirar (até 24h)."""
        self._limpar_sessao()
        self.erro = ""
        return rx.redirect("/login")
