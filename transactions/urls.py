"""
Reúne as urls da aplicação
"""

from django.urls import path
from .views import (
    dashboard_view,
    entradas_view,
    saidas_view,
    formulario_view,
    relatorios_view,
    historico_view,
    create_transaction,
    get_transactions,
    exportar_csv,
)


urlpatterns = [
    path("", dashboard_view, name="dashboard"),
    path("entradas/", entradas_view, name="entradas"),
    path("saidas/", saidas_view, name="saidas"),
    path("relatorios/", relatorios_view, name="relatorios"),
    path("historico/", historico_view, name="historico"),
    path("create/", create_transaction, name="create"),
    path("list/", get_transactions, name="transactions"),
    path("form/", formulario_view, name="form"),
    path("export/", exportar_csv, name="exportar_csv"),
]
