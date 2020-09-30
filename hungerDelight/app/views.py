from django.shortcuts import render
from .serializers import MerchantSerializer, StoreSerializer, ItemSerializer, OrderSerializer
from .models import Merchant, Store, Item, Order
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class MerchantViewSet(viewsets.ModelViewSet):
    serializer_class = MerchantSerializer
    queryset = Merchant.objects.all()
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]


class StoreViewSet(viewsets.ModelViewSet):
    serializer_class = StoreSerializer
    queryset = Store.objects.all()
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
