from django.urls import path
from . import views

urlpatterns = [
    path("produtos/", views.produtos, name="produtos"),
    path("carrinho/", views.carrinho, name="carrinho"),
    path("checkout/", views.checkout, name="checkout"),
]
