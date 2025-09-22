from django.test import TestCase
from django.urls import reverse
from store.models import Produto

class HomePageTests(TestCase):
    def setUp(self):
        # Criamos 4 produtos mockados no banco de teste
        self.produto1 = Produto.objects.create(
            nome="Notebook Gamer",
            preco=4500.00,
            descricao="Notebook rápido para jogos",
        )
        self.produto2 = Produto.objects.create(
            nome="Mouse sem fio",
            preco=150.00,
            descricao="Mouse leve e confortável",
        )
        self.produto3 = Produto.objects.create(
            nome="Teclado Mecânico",
            preco=350.00,
            descricao="Teclado com switches rápidos",
        )
        self.produto4 = Produto.objects.create(
            nome="Monitor 27\" 144Hz",
            preco=1200.00,
            descricao="Monitor para jogos com alta taxa de atualização",
        )

    def test_home_page_status_code(self):
        """A página inicial deve responder com 200"""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_home_page_mostra_produtos(self):
        """A home deve mostrar os nomes de todos os produtos"""
        response = self.client.get(reverse("home"))
        for produto in [self.produto1, self.produto2, self.produto3, self.produto4]:
            self.assertContains(response, produto.nome)

    def test_home_page_precos(self):
        """A home deve mostrar o preço dos produtos"""
        response = self.client.get(reverse("home"))
        for produto in [self.produto1, self.produto2, self.produto3, self.produto4]:
            self.assertContains(response, f"R${produto.preco:.2f}")


class CarrinhoPageTests(TestCase):
    def setUp(self):
        # Criamos produtos para o carrinho
        self.produto1 = Produto.objects.create(
            nome="Notebook Gamer",
            preco=4500.00,
            descricao="Notebook rápido para jogos",
        )
        self.produto2 = Produto.objects.create(
            nome="Mouse sem fio",
            preco=150.00,
            descricao="Mouse leve e confortável",
        )

    def test_carrinho_vazio(self):
        """Se o carrinho estiver vazio, deve exibir a mensagem padrão"""
        response = self.client.get(reverse("carrinho"))
        self.assertContains(response, "Por enquanto está vazio...")

    def test_adicionar_produto_carrinho(self):
        """Adicionar produto ao carrinho deve mostrar no template"""
        session = self.client.session
        session['carrinho'] = {str(self.produto1.id): {'quantidade': 1, 'preco': str(self.produto1.preco)}}
        session.save()

        response = self.client.get(reverse("carrinho"))
        self.assertContains(response, "Notebook Gamer")
        self.assertNotContains(response, "Por enquanto está vazio...")

    def test_remover_produto_carrinho(self):
        """Remover produto do carrinho deve atualizar a sessão"""
        session = self.client.session
        session['carrinho'] = {
            str(self.produto1.id): {'quantidade': 1, 'preco': str(self.produto1.preco)},
            str(self.produto2.id): {'quantidade': 1, 'preco': str(self.produto2.preco)},
        }
        session.save()

        # Simular remoção
        del session['carrinho'][str(self.produto1.id)]
        session.save()

        response = self.client.get(reverse("carrinho"))
        self.assertNotContains(response, "Notebook Gamer")
        self.assertContains(response, "Mouse sem fio")