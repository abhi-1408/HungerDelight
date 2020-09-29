from django.db import models

# Create your models here.


class Merchants(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    mobile = models.CharField(max_length=10)


class Stores(models.Model):
    name = models.CharField(max_length=200)
    merchant = models.ForeignKey(Merchants, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    lat = models.FloatField()
    lng = models.FloatField()
    operational = models.BooleanField()


class Items(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    description = models.TextField()


class Orders(models.Model):
    totalAmount = models.FloatField()
    timeStamp = models.DateTimeField()
    store = models.ForeignKey(Stores, on_delete=models.CASCADE)
    merchant = models.ForeignKey(Merchants, on_delete=models.CASCADE)
    status = models.BooleanField()
    paymentMode = models.CharField(max_length=200)


class OrderItemMapping(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.IntegerField()
