# users/forms.py
from django import forms

class SignupForm(forms.Form):
    nome = forms.CharField(max_length=100, label="Nome")
    email = forms.EmailField(label="E-mail")
    senha = forms.CharField(widget=forms.PasswordInput(), label="Senha")
    telefone = forms.CharField(max_length=20, label="Telefone", required=False)
    is_vendor = forms.BooleanField(
        required=False, 
        label="Sou vendedor"
    )