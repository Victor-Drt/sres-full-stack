"""
    define os metodos de views da aplicação
"""
from django.shortcuts import render
# from django.http.response import HttpResponse

# Create your views here.
def dashboard(request):
    """
    view que renderiza o dashboard de transactions
    """
    return render(request, 'dashboard.html')

def entradas(request):
    """
    view que renderiza a pagina de entradas em transactions
    """
    return render(request, 'entradas.html')

def saidas(request):
    """
    view que renderiza a pagina de saidas em transactions
    """
    return render(request, 'saidas.html')

def relatorios(request):
    """
    view que renderiza a pagina de relatorios em transactions
    """
    return render(request, 'relatorios.html')

def historico(request):
    """
    view que renderiza a pagina de historico em transactions
    """
    return render(request, 'historico.html')

def login(request):
    """
    view que renderiza a pagina de login em transactions
    """
    return render(request, 'login.html')
