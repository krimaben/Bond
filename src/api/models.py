from django.db import models
from django.contrib.auth.models import User
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    MinLengthValidator,
)

# Create your models here.
class Bond(models.Model):
    BOND_STATUS_CHOICES = (("available", "AVAILABLE"), ("purchased", "PURCHASED"))
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_requests_seller_created"
    )
    publication_id = models.AutoField(primary_key=True)
    bond_name = models.CharField(validators=[MinLengthValidator(3)], max_length=40)
    number_of_bonds = models.IntegerField(
        validators=[MaxValueValidator(10000), MinValueValidator(1)]
    )
    sp_of_bonds = models.DecimalField(
        validators=[MaxValueValidator(100000000), MinValueValidator(0)],
        decimal_places=4,
        max_digits=13,
    )
    status_of_bond = models.CharField(
        max_length=10, default="Available", choices=BOND_STATUS_CHOICES, blank=True
    )
    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="%(class)s_requests_buyer_created",
    )
    usd_rates = models.DecimalField(
        decimal_places=4, max_digits=13, blank=True, null=True
    )
