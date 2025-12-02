from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from unittest.mock import patch, Mock


# ============================================================
#  MOCK GLOBAL: Evita qualquer chamada real ao backend
# ============================================================

def mock_api_get_success(*args, **kwargs):
    return []


# ============================================================
#  HOME / PRODUTOS
# ============================================================

class HomeViewTests(TestCase):

    @patch("store.views.get")
    def test_home_lista_produtos(self, mock_get):
        mock_get.return_value = [
            {"id": 1, "nome": "Produto A", "descricao": "Teste", "preco": 50, "estoque": 10}
        ]

        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Produto A")

    @patch("store.views.get")
    def test_home_busca_produtos(self, mock_get):
        mock_get.return_value = []

        response = self.client.get(reverse("home") + "?q=Mouse")

        mock_get.assert_called_with("/produtos/?q=Mouse")
        self.assertEqual(response.status_code, 200)


class ProdutosViewTests(TestCase):

    @patch("store.views.get")
    def test_produtos_sem_filtro(self, mock_get):
        mock_get.return_value = []

        self.client.get(reverse("produtos"))
        mock_get.assert_called_with("/produtos/")

    @patch("store.views.get")
    def test_produtos_com_filtro(self, mock_get):
        mock_get.return_value = []

        self.client.get(reverse("produtos") + "?q=Teclado")
        mock_get.assert_called_with("/produtos/?q=Teclado")


# ============================================================
#  DETALHES DO PRODUTO
# ============================================================

class ProdutoDetalhesTests(TestCase):

    @patch("store.views.get")
    def test_produto_detalhes_existente(self, mock_get):
        mock_get.return_value = {"id": 1, "nome": "Produto X"}

        response = self.client.get(reverse("produto_detalhes", args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Produto X")

    @patch("store.views.get")
    def test_produto_detalhes_inexistente(self, mock_get):
        mock_get.return_value = None

        response = self.client.get(reverse("produto_detalhes", args=[999]), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Produto não encontrado")


# ============================================================
#  CARRINHO
# ============================================================

class CarrinhoTests(TestCase):

    def test_carrinho_sem_login(self):
        response = self.client.get(reverse("carrinho"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("login"))

    @patch("store.views.get")
    def test_carrinho_logado(self, mock_get):
        mock_get.return_value = {
            "itens": [
                {"produto_nome": "Mouse", "produto_preco": 30, "quantidade": 2}
            ]
        }

        session = self.client.session
        session["usuario"] = {"id": 1, "nome": "Teste"}
        session.save()

        response = self.client.get(reverse("carrinho"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mouse")
        self.assertContains(response, "60.00")


# ============================================================
#  CHECKOUT
# ============================================================

class CheckoutTests(TestCase):

    @patch("store.views.get")
    def test_checkout_logado(self, mock_get):
        mock_get.return_value = {
            "itens": [
                {"produto_preco": 10, "quantidade": 3}
            ]
        }

        session = self.client.session
        session["usuario"] = {"id": 1}
        session.save()

        resp = self.client.get(reverse("checkout"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "30.00")

    def test_checkout_sem_login(self):
        resp = self.client.get(reverse("checkout"))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, reverse("login"))


# ============================================================
#  FINALIZAR COMPRA
# ============================================================

class FinalizarCompraTests(TestCase):

    @patch("store.views.requests.post")
    def test_finalizar_sucesso(self, mock_post):
        session = self.client.session
        session["usuario"] = {"id": 1}
        session.save()

        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_post.return_value = mock_resp

        resp = self.client.post(reverse("finalizar_compra"), follow=True)

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Compra finalizada com sucesso")

    @patch("store.views.requests.post")
    def test_finalizar_erro_backend(self, mock_post):
        session = self.client.session
        session["usuario"] = {"id": 1}
        session.save()

        mock_resp = Mock()
        mock_resp.status_code = 400
        mock_resp.json.return_value = {"detail": "Erro!"}
        mock_post.return_value = mock_resp

        resp = self.client.post(reverse("finalizar_compra"), follow=True)
        self.assertContains(resp, "Erro!")


# ============================================================
#  ADICIONAR AO CARRINHO
# ============================================================

class AdicionarCarrinhoTests(TestCase):

    @patch("store.views.requests.post")
    def test_add_carrinho_sucesso(self, mock_post):
        session = self.client.session
        session["usuario"] = {"id": 1}
        session.save()

        mock_post.return_value.status_code = 200

        resp = self.client.post(reverse("adicionar_ao_carrinho", args=[5]))
        self.assertEqual(resp.status_code, 302)

    def test_add_carrinho_sem_login(self):
        resp = self.client.post(reverse("adicionar_ao_carrinho", args=[1]), follow=True)
        self.assertContains(resp, "Você precisa estar logado.")


# ============================================================
#  PERMISSÃO PARA PRODUTOS
# ============================================================

class PermissaoProdutoTests(TestCase):

    def test_add_produto_sem_permissao(self):
        resp = self.client.get(reverse("adicionar_produto"), follow=True)
        self.assertContains(resp, "Acesso negado")

    def test_remover_produto_sem_permissao(self):
        resp = self.client.get(reverse("remover_produto"), follow=True)
        self.assertContains(resp, "Acesso negado")

    @patch("store.views.get")
    def test_add_produto_permitido(self, mock_get):
        session = self.client.session
        session["usuario"] = {"id": 1, "is_vendor": True}
        session.save()

        resp = self.client.get(reverse("adicionar_produto"))
        self.assertEqual(resp.status_code, 200)

    @patch("store.views.get")
    def test_remover_produto_permitido(self, mock_get):
        session = self.client.session
        session["usuario"] = {"id": 1, "is_admin": True}
        session.save()

        mock_get.return_value = []
        resp = self.client.get(reverse("remover_produto"))
        self.assertEqual(resp.status_code, 200)


# ============================================================
#  REMOVER PRODUTO
# ============================================================

class RemoverProdutoTests(TestCase):

    @patch("store.views.requests.delete")
    def test_remover_produto_sucesso(self, mock_delete):
        session = self.client.session
        session["usuario"] = {"id": 1, "is_vendor": True}
        session.save()

        mock_resp = Mock()
        mock_resp.status_code = 204
        mock_delete.return_value = mock_resp

        resp = self.client.post(reverse("remover_produto_confirmar", args=[10]), follow=True)

        self.assertContains(resp, "Produto removido com sucesso")

    @patch("store.views.requests.delete")
    def test_remover_produto_erro(self, mock_delete):
        session = self.client.session
        session["usuario"] = {"id": 1, "is_admin": True}
        session.save()

        mock_resp = Mock()
        mock_resp.status_code = 400
        mock_resp.text = "Falha"
        mock_delete.return_value = mock_resp

        resp = self.client.post(reverse("remover_produto_confirmar", args=[10]), follow=True)

        self.assertContains(resp, "Erro ao remover produto")
