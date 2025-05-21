from django.db import models

# Create your models here.
class Transaction(models.Model):
    TYPE_TRANSACTION = [
        ('DIZIMO', 'Dízimo'),
        ('OFERTA', 'Oferta'),
        ('SAIDA', 'Saída'),
    ]

    description = models.CharField(max_length=100, blank=True, null=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateField()
    transaction_type = models.CharField(choices=TYPE_TRANSACTION, max_length=10)
    class Meta:
        ordering = ['-created_at']