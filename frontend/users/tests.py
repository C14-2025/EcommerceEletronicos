from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch, Mock
from users.forms import SignupForm

class LoginViewTests(TestCase):
    @patch("users.views.requests.post")
    def test_login_sucesso(self, mock_post):
        """Login com credenciais válidas deve redirecionar para a home e salvar usuário na sessão"""
        # Simula resposta bem-sucedida do backend FastAPI
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"usuario": {"nome": "Lucas", "email": "lucas@example.com"}}
        mock_post.return_value = mock_response

        response = self.client.post(reverse("login"), {"email": "lucas@example.com", "senha": "1234"})

        # Verifica redirecionamento para home
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("home"))

        # Verifica se o usuário foi salvo na sessão
        session = self.client.session
        self.assertIn("usuario", session)
        self.assertEqual(session["usuario"]["nome"], "Lucas")

    @patch("users.views.requests.post")
    def test_login_credenciais_invalidas(self, mock_post):
        """Login com credenciais inválidas deve exibir mensagem de erro"""
        # Simula resposta 401 do backend
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"detail": "Credenciais inválidas."}
        mock_post.return_value = mock_response

        response = self.client.post(reverse("login"), {"email": "lucas@example.com", "senha": "errada"}, follow=True)

        # Verifica que não houve redirecionamento
        self.assertEqual(response.status_code, 200)
        # Verifica se mensagem de erro foi renderizada
        self.assertContains(response, "Credenciais inválidas.")

    @patch("users.views.requests.post", side_effect=Exception("Servidor indisponível"))
    def test_login_falha_conexao_backend(self, mock_post):
        """Se o backend estiver fora do ar, deve exibir mensagem de erro amigável"""
        response = self.client.post(reverse("login"), {"email": "lucas@example.com", "senha": "1234"}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Erro ao conectar com o backend")

    def test_login_campos_vazios(self):
        """Se os campos não forem preenchidos, deve redirecionar para a página de login"""
        response = self.client.post(reverse("login"), {"email": "", "senha": ""})

        # A view redireciona com messages.error
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("login"))


# ---------------------------------------------------------
# 1) TESTE DO CADASTRO (SIGNUP) COM SUCESSO
# ---------------------------------------------------------
class SignupTests(TestCase):
    @patch("users.views.requests.post")
    def test_signup_sucesso(self, mock_post):
        """Usuário deve ser cadastrado com sucesso e redirecionado para login"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_post.return_value = mock_response

        data = {
            "nome": "Luiz",
            "email": "luiz@example.com",
            "senha": "1234",
            "telefone": "123456789",
            "is_vendor": False
        }

        response = self.client.post(reverse("signup"), data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("login"))

    # ---------------------------------------------------------
    # 2) TESTE DE FALHA NA API DURANTE CADASTRO
    # ---------------------------------------------------------
    @patch("users.views.requests.post", side_effect=Exception("Servidor offline"))
    def test_signup_erro_backend(self, mock_post):
        """Exibe mensagem amigável quando o backend está offline no cadastro"""
        response = self.client.post(reverse("signup"), {
            "nome": "Teste",
            "email": "teste@example.com",
            "senha": "1234"
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Falha de conexão com o servidor")


# ---------------------------------------------------------
# 3) TESTE DO FORM DE CADASTRO
# ---------------------------------------------------------
class SignupFormTests(TestCase):
    def test_form_signup_valido(self):
        """Formulário de signup deve ser válido com dados corretos"""
        form = SignupForm(data={
            "nome": "Lucas",
            "email": "lucas@example.com",
            "senha": "1234",
            "telefone": "",
            "is_vendor": False
        })

        self.assertTrue(form.is_valid())

    def test_form_signup_invalido_email(self):
        """Formulário deve ser inválido quando o email é incorreto"""
        form = SignupForm(data={
            "nome": "Lucas",
            "email": "email_invalido",
            "senha": "1234"
        })

        self.assertFalse(form.is_valid())


# ---------------------------------------------------------
# 4) TESTE DE LOGOUT
# ---------------------------------------------------------
class LogoutTests(TestCase):
    def test_logout_limpa_sessao(self):
        """Logout deve remover o usuário da sessão e redirecionar para home"""
        session = self.client.session
        session["usuario"] = {"nome": "Teste"}
        session.save()

        response = self.client.get(reverse("logout"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("home"))

        session = self.client.session
        self.assertNotIn("usuario", session)


# ---------------------------------------------------------
# 5) TESTE DE MUDANÇA DE SENHA – SENHA ATUAL INCORRETA
# ---------------------------------------------------------
class MudarSenhaTests(TestCase):
    @patch("users.views.requests.post")
    def test_mudar_senha_incorreta(self, mock_post):
        """Se a senha atual estiver errada, deve exibir erro"""
        session = self.client.session
        session["usuario"] = {"id": 1, "email": "teste@example.com"}
        session.save()

        mock_response = Mock()
        mock_response.status_code = 401
        mock_post.return_value = mock_response

        resp = self.client.post(reverse("mudar_senha"), {
            "senha_atual": "errada",
            "nova_senha": "nova123",
            "confirmar": "nova123"
        }, follow=True)

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Senha atual incorreta")


# ---------------------------------------------------------
# 6) TESTE DE DELETAR CONTA
# ---------------------------------------------------------
class DeletarContaTests(TestCase):
    @patch("users.views.requests.delete")
    def test_deletar_conta_sucesso(self, mock_delete):
        """Usuário deve conseguir deletar conta com sucesso"""
        session = self.client.session
        session["usuario"] = {"id": 1, "email": "teste@example.com"}
        session.save()

        mock_response = Mock()
        mock_response.status_code = 204
        mock_delete.return_value = mock_response

        response = self.client.post(reverse("deletar_conta"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("home"))
