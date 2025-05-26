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


# Create your views here.
def dashboard(request):
    """
    view que renderiza o dashboard de transactions
    """

    if not request.user.is_authenticated:
        return redirect('login')

    transactions = Transaction.objects.all()

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


def formulario(request):
    
    if not request.user.is_authenticated:
        return redirect('login')
    
    form = TransactionForm()
    return render(request, "form_transaction.html", {"form": form})


def get_transactions(request):
    grouped = (
        Transaction.objects.annotate(
            month=TruncMonth("created_at"),
            tipo_financeiro=Case(
                When(transaction_type__in=["DIZIMO", "OFERTA"], then=Value("ENTRADA")),
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


def entradas(request):
    """
    view que renderiza a pagina de entradas em transactions
    """
    if not request.user.is_authenticated:
        return redirect('login')
    transactions = Transaction.objects.filter(transaction_type__in=["OFERTA", "DIZIMO"])
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

            transaction = Transaction.objects.create(
                description=description,
                value=value,
                transaction_type=transaction_type,
                created_at=created_at,
            )

            if transaction_type == "SAIDA":
                return redirect("saidas")
    return redirect("entradas")


def saidas(request):
    """
    view que renderiza a pagina de saidas em transactions
    """
    if not request.user.is_authenticated:
        return redirect('login')
    transactions = Transaction.objects.filter(transaction_type__in=["SAIDA"])
    return render(request, "saidas.html", {"transactions": transactions})


def relatorios(request):
    """
    view que renderiza a pagina de relatorios em transactions
    """
    if not request.user.is_authenticated:
        return redirect('login')
    form = ReportForm()
    transactions = Transaction.objects.all()

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


def historico(request):
    """
    view que renderiza a pagina de historico em transactions
    """
    if not request.user.is_authenticated:
        return redirect('login')
    transactions = Transaction.objects.all()

    return render(request, "historico.html", {"transactions": transactions})

