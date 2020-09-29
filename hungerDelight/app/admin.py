from django.contrib import admin
from app.models import Merchants, Stores, Items, Orders, OrderItemMapping

# Register your models here.
admin.site.register(Merchants)
admin.site.register(Stores)
admin.site.register(Items)
admin.site.register(Orders)
admin.site.register(OrderItemMapping)
