from django.contrib import admin
from app.models import Merchant, Store, Item, Order


# Register your models here.
admin.site.register(Merchant)
admin.site.register(Store)
admin.site.register(Item)
admin.site.register(Order)
