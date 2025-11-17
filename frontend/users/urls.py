from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),
    path("mudar-senha/", views.mudar_senha, name="mudar_senha"),
    path("deletar-conta/", views.deletar_conta, name="deletar_conta"),
]

