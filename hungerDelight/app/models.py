from django.db import models

# Create your models here.


class Merchants(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    mobile = models.CharField(max_length=10)


class Stores(models.Model):
    name = models.CharField(max_length=255)
    merchant = models.ForeignKey(
        'Merchants',
        on_delete=models.CASCADE,
    )
    address = models.CharField(max_length=255)
    lat = models.DecimalField(max_digits=18, decimal_places=15)
    lng = models.DecimalField(max_digits=18, decimal_places=15)
    operational = models.BooleanField()


class Items(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=15, decimal_places=6)
    created_at = models.DateTimeField()
    description = models.TextField(null=True)


class Orders(models.Model):
    totalAmount = models.DecimalField(max_digits=19, decimal_places=6)
    timeStamp = models.DateTimeField()
    store = models.ForeignKey(
        'Stores',
        on_delete=models.CASCADE
    )
    merchant = models.ForeignKey(
        'Merchants',
        on_delete=models.CASCADE
    )
    status = models.BooleanField()
    paymentMode = models.CharField(max_length=255)


class OrderItemMapping(models.Model):
    order = models.ForeignKey(
        'Orders',
        on_delete=models.CASCADE
    )
    item = models.ForeignKey(
        'Items',
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField()
