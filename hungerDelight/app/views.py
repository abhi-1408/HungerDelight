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
def merchant_list_view(request):
    merchants = Merchant.objects.all()
    merchant_serializer = MerchantSerializer(merchants, many=True)
    return Response(merchant_serializer.data)


@api_view(['GET'])
def merchant_detail_view(request, pk):
    merchants = Merchant.objects.get(id=pk)
    merchant_serializer = MerchantSerializer(merchants, many=False)
    return Response(merchant_serializer.data)


@api_view(['GET'])
def store_list_view(request):
    stores = Store.objects.all()
    store_serializer = StoreSerializer(stores, many=True)
    return Response(store_serializer.data)


@api_view(['GET'])
def store_detail_view(request, pk):
    stores = Store.objects.get(id=pk)
    store_serializer = StoreSerializer(stores, many=False)
    return Response(store_serializer.data)


@api_view(['GET'])
def item_list_view(request):
    items = Item.objects.all()
    item_serializer = ItemSerializer(items, many=True)
    return Response(item_serializer.data)


@api_view(['GET'])
def item_detail_view(request, pk):
    items = Item.objects.get(id=pk)
    item_serializer = ItemSerializer(items, many=False)
    return Response(item_serializer.data)
