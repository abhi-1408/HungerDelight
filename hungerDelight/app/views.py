from django.shortcuts import render
from .serializers import MerchantSerializer, StoreSerializer, ItemSerializer, OrderSerializer, OrderSerializerAll
from .models import Merchant, Store, Item, Order
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .tasks import create_order
import structlog
logger = structlog.get_logger()
# Create your views here.


class MerchantViewSet(viewsets.ModelViewSet):
    serializer_class = MerchantSerializer
    queryset = Merchant.objects.all()
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        logger.msg('Create Merchant Request', req=request)
        return response

    @action(detail=True, methods=['get'])
    def item(self, request, pk=None):
        # get details of the merchant
        merchant_data = Merchant.objects.filter(id=pk).first()
        serialized_merchant_data = MerchantSerializer(
            merchant_data, many=False)

        # to get the all items belonging to the merchant
        all_item_of_same_merchant = Item.objects.filter(merchant_id=pk).all()
        serialized_all_item_of_same_merchant = ItemSerializer(
            all_item_of_same_merchant, many=True)

        return Response({"merchant": serialized_merchant_data.data, "items": serialized_all_item_of_same_merchant.data})

    @action(detail=True, methods=['get'])
    def store(self, request, pk=None):
        # get details of the merchant
        merchant_data = Merchant.objects.filter(id=pk).first()
        serialized_merchant_data = MerchantSerializer(
            merchant_data, many=False)

        # to get the all stores belonging to the merchant
        all_store_of_a_merchant = Store.objects.filter(merchant_id=pk).all()
        serialized_all_store_of_a_merchant = StoreSerializer(
            all_store_of_a_merchant, many=True)

        return Response({"merchant": serialized_merchant_data.data, "stores": serialized_all_store_of_a_merchant.data})

    @action(detail=True, methods=['get'])
    def order(self, request, pk=None):
        # get details of the merchant
        merchant_data = Merchant.objects.filter(id=pk).first()
        serialized_merchant_data = MerchantSerializer(
            merchant_data, many=False)

        # to get all order placed for a merchant
        all_order_placed_for_merchant = Order.objects.filter(
            merchant_id=pk).all()
        serialized_all_order_placed_for_merchant = OrderSerializer(
            all_order_placed_for_merchant, many=True)

        return Response({"merchant": serialized_merchant_data.data, "orders": serialized_all_order_placed_for_merchant.data})


class StoreViewSet(viewsets.ModelViewSet):
    serializer_class = StoreSerializer
    queryset = Store.objects.all()
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        logger.msg('Create Store Request', req=request)
        return response

    @action(detail=True, methods=['get'])
    def order(self, request, pk=None):
        # get details of the Store
        store_data = Store.objects.filter(id=pk).first()
        serialized_store_data = StoreSerializer(
            store_data, many=False)

        # to get all order placed for a store
        all_order_placed_for_store = Order.objects.filter(
            store_id=pk).all()
        serialized_all_order_placed_for_store = OrderSerializer(
            all_order_placed_for_store, many=True)

        return Response({"store": serialized_store_data.data, "orders": serialized_all_order_placed_for_store.data})

    @action(detail=True, methods=['get'])
    def item(self, request, pk=None):
        # get details of the Store
        store_data = Store.objects.filter(id=pk).first()
        serialized_store_data = StoreSerializer(
            store_data, many=False)

        # to get all item in a store
        merchant_id = serialized_store_data.data['merchant']
        print('MERCHANT ID', serialized_store_data.data['merchant'])
        all_items_in_a_store = Item.objects.filter(
            merchant_id=merchant_id).all()
        serialized_all_items_in_a_store = ItemSerializer(
            all_items_in_a_store, many=True)

        return Response({"store": serialized_store_data.data, "items": serialized_all_items_in_a_store.data})


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        logger.msg('Create Item Request', req=request)
        return response


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = Order.objects.all()
        serializer = OrderSerializerAll(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        # print('created data', dir(self), dir(request))
        # print('data is ', request.POST)

        log = logger.bind(status='Created order request', req=request)

        # print('request data: ', request.data)
        serializer_order = OrderSerializer(data=request.data)

        if serializer_order.is_valid():
            # print('serialized ', serializer_order.data)
            create_order.delay(serializer_order.data)
            # serializer_order.save()
            log.msg('Create order taken successfully, order is being processed',
                    status="Create request successful")
            return Response({'message': 'order is being processed'})

        # serialized data from request
        # serialized data isvalid
        # async tasks -  apply_async
        # order will be processed
        return Response({'message': 'bad request'})
