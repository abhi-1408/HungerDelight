from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import MerchantSerializer, StoreSerializer, ItemSerializer
from .models import Merchant, Store, Item
# Create your views here.


@api_view(['GET'])
def index(request):
    return Response('HI EVERYONE')


@api_view(['GET'])
def all_merchant_view(request):
    merchants = Merchant.objects.all()
    merchant_serializer = MerchantSerializer(merchants, many=True)

    return Response(merchant_serializer.data)


@api_view(['GET'])
def all_store_view(request):
    stores = Store.objects.all()
    store_serializer = StoreSerializer(stores, many=True)

    return Response(store_serializer.data)


@api_view(['GET'])
def all_item_view(request):
    items = Item.objects.all()
    item_serializer = ItemSerializer(items, many=True)

    return Response(item_serializer.data)
