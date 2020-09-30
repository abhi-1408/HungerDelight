from django.shortcuts import render
from .serializers import MerchantSerializer, StoreSerializer, ItemSerializer
from .models import Merchant, Store, Item
from rest_framework import viewsets
# Create your views here.


class MerchantViewSet(viewsets.ModelViewSet):
    serializer_class = MerchantSerializer
    queryset = Merchant.objects.all()


class StoreViewSet(viewsets.ModelViewSet):
    serializer_class = StoreSerializer
    queryset = Store.objects.all()


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
