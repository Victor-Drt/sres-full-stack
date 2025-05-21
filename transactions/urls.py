"""
    Reúne as urls da aplicação
"""

from django.urls import path
from .views import dashboard, entradas, saidas, relatorios, historico, create_transaction, get_transactions


urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('entradas/', entradas, name='entradas'),
    path('saidas/', saidas, name='saidas'),
    path('relatorios/', relatorios, name='relatorios'),
    path('historico/', historico, name='historico'),
    path('create/', create_transaction, name='create'),
    path('list/', get_transactions, name='transactions'),
]
