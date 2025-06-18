"""
define os metodos de views da aplicação
"""

from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.db.models.functions import TruncMonth
from .models import Transaction
from django.db.models import Sum, Case, When, Value, CharField
from django.views.decorators.csrf import csrf_exempt
from .forms import TransactionForm, ReportForm
import csv
from django.http import HttpResponse


# Create your views here.
def dashboard_view(request):
    """
    view que renderiza o dashboard de transactions
    """
    user = request.user

    if not user.is_authenticated:
        return redirect('login')

    transactions = Transaction.objects.filter(user=user)

    total_dizimos = (
        transactions.filter(transaction_type="DIZIMO")
        .aggregate(total=Sum("value"))
        .get("total")
        or 0
    )
    total_ofertas = (
        transactions.filter(transaction_type="OFERTA")
        .aggregate(total=Sum("value"))
        .get("total")
        or 0
    )
    total_saida = (
        transactions.filter(transaction_type="SAIDA")
        .aggregate(total=Sum("value"))
        .get("total")
        or 0
    )
    total = total_dizimos + total_ofertas - total_saida

    response = {
        "total_dizimos": total_dizimos,
        "total_ofertas": total_ofertas,
        "total_saida": total_saida,
        "total": total,
    }

    return render(request, "dashboard.html", response)


def formulario_view(request):
    """
    view que renderiza e valida o formulario de criação de nova transação.
    """

    if not request.user.is_authenticated:
        return redirect('login')

    form = TransactionForm()
    return render(request, "form_transaction.html", {"form": form})


def get_transactions(request):
    """
    metodo que retorna as informaçoes resumidas para o dashboard
    """
    transactions = Transaction.objects.filter(user=request.user)

    grouped = (
        transactions.annotate(
            month=TruncMonth("created_at"),
            tipo_financeiro=Case(
                When(transaction_type__in=["DIZIMO", "OFERTA"], then=Value(
                    "ENTRADA"
                )),
                When(transaction_type="SAIDA", then=Value("SAIDA")),
                default=Value("OUTRO"),
                output_field=CharField(),
            ),
        )
        .values("month", "tipo_financeiro")
        .annotate(total=Sum("value"))
        .order_by("month")
    )

    data = [
        {
            "month": item["month"].strftime("%m"),
            "tipo": item["tipo_financeiro"],
            "total": float(item["total"]),
        }
        for item in grouped
    ]

    months = list(set(item["month"] for item in data))

    response = {
        "months": months,
        "data": data,
    }

    return JsonResponse(response, safe=False)


def entradas_view(request):
    """
    view que renderiza a pagina de entradas em transactions
    """
    if not request.user.is_authenticated:
        return redirect('login')
    transactions = Transaction.objects.filter(
        user=request.user, transaction_type__in=["OFERTA", "DIZIMO"]
    )
    return render(request, "entradas.html", {"transactions": transactions})


@csrf_exempt
def create_transaction(request):
    """
    metodo chamado para criação de transaction
    """
    if request.method == "POST":

        form = TransactionForm(request.POST)

        if form.is_valid():
            description = form.cleaned_data["description"]
            value = form.cleaned_data["value"]
            transaction_type = form.cleaned_data["type"]
            created_at = form.cleaned_data["created_at"]

            Transaction.objects.create(
                description=description,
                value=value,
                transaction_type=transaction_type,
                created_at=created_at,
                user=request.user
            )

            if transaction_type == "SAIDA":
                return redirect("saidas")
    return redirect("entradas")


def saidas_view(request):
    """
    view que renderiza a pagina de saidas em transactions
    """
    if not request.user.is_authenticated:
        return redirect('login')
    transactions = Transaction.objects.filter(
        user=request.user, transaction_type__in=["SAIDA"]
    )
    return render(request, "saidas.html", {"transactions": transactions})


def relatorios_view(request):
    """
    view que renderiza a pagina de relatorios em transactions
    """
    if not request.user.is_authenticated:
        return redirect('login')

    form = ReportForm(request.POST or None)
    transactions = Transaction.objects.filter(user=request.user)

    if form.is_valid():
        start = form.cleaned_data["start"]
        end = form.cleaned_data["end"]
        transactions = transactions.filter(created_at__range=(start, end))

    total_dizimos = (
        transactions.filter(transaction_type="DIZIMO")
        .aggregate(total=Sum("value"))
        .get("total")
        or 0
    )
    total_ofertas = (
        transactions.filter(transaction_type="OFERTA")
        .aggregate(total=Sum("value"))
        .get("total")
        or 0
    )
    total_saida = (
        transactions.filter(transaction_type="SAIDA")
        .aggregate(total=Sum("value"))
        .get("total")
        or 0
    )
    total = total_dizimos + total_ofertas - total_saida

    response = {
        "total_dizimos": total_dizimos,
        "total_ofertas": total_ofertas,
        "total_saida": total_saida,
        "total": total,
        "form": form,
    }

    return render(request, "relatorios.html", response)

def exportar_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="relatorio_financeiro.csv"'

    writer = csv.writer(response)
    writer.writerow(['Data', 'Tipo', 'Valor'])

    transacoes = Transaction.objects.filter(user=request.user)

    total_dizimos = 0
    total_ofertas = 0
    total_saidas = 0

    for transacao in transacoes:
        writer.writerow([transacao.created_at, transacao.transaction_type, transacao.value])
        if transacao.transaction_type == 'DIZIMO':
            total_dizimos += transacao.value
        elif transacao.transaction_type == 'OFERTA':
            total_ofertas += transacao.value
        elif transacao.transaction_type == 'SAIDA':
            total_saidas += transacao.value

    writer.writerow([])
    writer.writerow(['Total de Dízimos', total_dizimos])
    writer.writerow(['Total de Ofertas', total_ofertas])
    writer.writerow(['Total de Saídas', total_saidas])
    writer.writerow(['Saldo Final', total_dizimos + total_ofertas - total_saidas])

    return response

def historico_view(request):
    """
    view que renderiza a pagina de historico em transactions
    """
    if not request.user.is_authenticated:
        return redirect('login')
    transactions = Transaction.objects.filter(user=request.user)

    return render(request, "historico.html", {"transactions": transactions})
