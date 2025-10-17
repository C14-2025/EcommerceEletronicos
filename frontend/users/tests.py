from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch, Mock

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

