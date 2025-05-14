"""
    Reúne as urls da aplicação
"""

from django.urls import path
from .views import dashboard, entradas, saidas, relatorios, historico, login


urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('entradas/', entradas, name='entradas'),
    path('saidas/', saidas, name='saidas'),
    path('relatorios/', relatorios, name='relatorios'),
    path('historico/', historico, name='historico'),
]
