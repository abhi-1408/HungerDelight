from django.db import models
from datetime import datetime

# Create your models here.


class Merchant(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    mobile = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=15, decimal_places=6)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    merchant = models.ForeignKey(
        'Merchant',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Store(models.Model):
    name = models.CharField(max_length=255)
    merchant = models.ForeignKey(
        'Merchant',
        on_delete=models.CASCADE,
    )
    items = models.ManyToManyField(Item)
    address = models.CharField(max_length=255)
    lat = models.DecimalField(
        max_digits=18, decimal_places=15, verbose_name='latitude')
    lng = models.DecimalField(
        max_digits=18, decimal_places=15, verbose_name='longitude')
    operational = models.BooleanField()

    def __str__(self):
        return f'{self.merchant} - {self.name}'


class Order(models.Model):
    payment_modes = (
        ('CASH', 'Cash'),
        ('CARD', 'Card'),
        ('WALLET', 'Wallet'),
        ('NET BANKING', 'Net Banking')
    )

    status_codes = (
        ('AWAITING', 'Awaiting'),
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed')
    )

    totalAmount = models.DecimalField(max_digits=19, decimal_places=6)
    total_items = models.PositiveIntegerField()
    timeStamp = models.DateTimeField(default=datetime.now, blank=True)
    store = models.ForeignKey(
        'Store',
        on_delete=models.CASCADE
    )
    merchant = models.ForeignKey(
        'Merchant',
        on_delete=models.CASCADE
    )
    items = models.ManyToManyField(Item)
    status = models.CharField(
        max_length=100, choices=status_codes, default='SUCCESS')
    paymentMode = models.CharField(
        max_length=255, choices=payment_modes, default='CASH')

    def __str__(self):
        return f'Orderid: {self.id} : from: {self.merchant} - {self.store}'
