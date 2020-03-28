from django.contrib import admin

# Register your models here.
from covid19help.commodity.models import Commodity, Category

admin.site.register(Commodity)
admin.site.register(Category)
