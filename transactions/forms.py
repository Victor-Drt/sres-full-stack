from django import forms
import datetime


class TransactionForm(forms.Form):
    TYPE_TRANSACTION = [
        ("DIZIMO", "Dízimo"),
        ("OFERTA", "Oferta"),
        ("SAIDA", "Saída"),
    ]

    description = forms.CharField(
        label="Descrição",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Descrição'}),
    )
    value = forms.DecimalField(
        max_digits=8,
        decimal_places=2,
        widget=forms.NumberInput(attrs={"class": "form-control", 'Ex: 0,00': 'Ex.: joaosilva@xpto.com'}),
    )
    type = forms.ChoiceField(
        choices=TYPE_TRANSACTION,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    created_at = forms.DateField(
        label="Data",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )

    def clean_value(self):
        value = self.cleaned_data["value"]
        if value < 0:
            raise forms.ValidationError("O valor não pode ser menor que 0")
        return value

    def clean_type(self):
        transaction_type = self.cleaned_data["type"]
        if transaction_type == "" or transaction_type is None:
            raise forms.ValidationError("O campo não pode estar vazio.")
        return transaction_type

    def clean_created_at(self):
        created_at = self.cleaned_data["created_at"]
        if created_at == "" or created_at == None:
            raise forms.ValidationError("O campo não pode estar vazio.")
        return created_at

class ReportForm(forms.Form):
        
    start = forms.DateField(
        label="De",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )
    
    end = forms.DateField(
        label="Até",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )
    
    def clean_start(self):
        start = self.cleaned_data["start"]
        if start == "" or start == None or start < self.end:
            raise forms.ValidationError("O campo não pode estar vazio. Ou data inicial não pode ser maior que a data final")
        return start
    
    def clean_end(self):
        end = self.cleaned_data["end"]
        if end == "" or end == None or end < self.start:
            raise forms.ValidationError("O campo não pode estar vazio. Ou data final não pode ser maior que a data inicial")
        return end