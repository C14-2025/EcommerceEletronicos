from django.test import TestCase
from django.urls import reverse
from store.models import Produto

class HomePageTests(TestCase):
    def setUp(self):
        # Criamos 2 produtos mockados no banco de teste
        self.produto1 = Produto.objects.create(
            nome="Notebook Gamer",
            preco=4500.00,
            descricao="Notebook rápido para jogos",
        )

    def test_home_page_status_code(self):
        """A página inicial deve responder com 200"""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)


class CarrinhoPageTests(TestCase):
    def test_carrinho_vazio(self):
        """Se o carrinho estiver vazio, deve exibir a mensagem padrão"""
        response = self.client.get(reverse("carrinho"))
        self.assertContains(response, "Por enquanto está vazio...")
