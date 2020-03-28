from django.contrib.auth.models import User
from django.db import models
from djmoney.models.fields import MoneyField

from covid19help.commodity.choices import CATEGORY_TYPE


class Category(models.Model):
    type = models.CharField(max_length=128, choices=CATEGORY_TYPE)
    other_name = models.CharField(null=True, blank=True)


class Commodity(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=512)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='category')
    owner = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE)
    has_price = models.NullBooleanField()
    is_donation = models.NullBooleanField()
    balance = MoneyField(max_digits=5, decimal_places=2, default_currency='USD')