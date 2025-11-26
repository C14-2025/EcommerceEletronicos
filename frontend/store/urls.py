from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("produtos/", views.produtos, name="produtos"),
    path("produto/<int:produto_id>/", views.produto_detalhes, name="produto_detalhes"),
    path("carrinho/", views.carrinho, name="carrinho"),
    path("checkout/", views.checkout, name="checkout"),
    path("checkout/finalizar/", views.finalizar_compra, name="finalizar_compra"),
    path("carrinho/adicionar/<int:produto_id>/", views.adicionar_ao_carrinho, name="adicionar_ao_carrinho"),
    path("perfil/", views.perfil, name="perfil"),
    path("meus-pedidos/", views.meus_pedidos, name="meus_pedidos"),
    path("produtos/adicionar/", views.adicionar_produto_page, name="adicionar_produto"),
    path("produtos/remover/", views.remover_produto_page, name="remover_produto"),
    path("produtos/remover/<int:produto_id>/", views.remover_produto, name="remover_produto_confirmar"),
]
