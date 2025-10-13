from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("produtos/", views.produtos, name="produtos"),
    path("carrinho/", views.carrinho, name="carrinho"),
    path("checkout/", views.checkout, name="checkout"),
    path("carrinho/adicionar/<int:produto_id>/", views.adicionar_ao_carrinho, name="adicionar_ao_carrinho"),
]
