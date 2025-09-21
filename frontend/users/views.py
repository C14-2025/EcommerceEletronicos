from django.http import HttpResponse

def login_view(request):
    return HttpResponse("Página de login (placeholder)")

def signup_view(request):
    return HttpResponse("Página de cadastro (placeholder)")

def logout_view(request):
    return HttpResponse("Logout (placeholder)")
