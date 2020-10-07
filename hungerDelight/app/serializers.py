from rest_framework import serializers
from .models import Merchant, Store, Item, Order
import json
from decimal import Decimal
from django.http import QueryDict


class MerchantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Merchant
        fields = '__all__'


class StoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Store
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = '__all__'


class OrderSerializerAll(serializers.ModelSerializer):
    '''
    To display all fields in request while for form need to display only certain fields
    '''

    class Meta:
        model = Order
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    '''
    For form display
    '''

    class Meta:
        model = Order
        # fields = '__all__'
        fields = ('id', 'timestamp', 'status', 'payment_mode',
                  'store', 'merchant', 'items')

    '''
    performing calculation for total price, total items before saving
    '''

    def create(self, validated_data):

        log.msg('Create Order Request', req=self)

        item_set = validated_data.pop('items', [])
        total_items = len(item_set)
        total_price = 0.0
        for item in item_set:
            total_price += float(item.price)

        validated_data['total_items'] = total_items
        validated_data['total_amount'] = total_price

        order = Order.objects.create(**validated_data)
        for item in item_set:
            order.items.add(item)
        order.save()
        print('in created of serializer *********')
        return order

    def validate_store(self, store):
        '''
        Checks if the store selected belong to the merchant or not

        '''
        # get in dict format if request from postman
        # converting dict to query dict
        query_dict = QueryDict('', mutable=True)
        query_dict.update(self.initial_data)
        self.initial_data = query_dict

        data_store_id = int(self.initial_data.get('store', default=None))
        data_merchant_id = int(self.initial_data.get('merchant', default=None))

        stores = Store.objects.filter(id=data_store_id).first()

        store_serialize = StoreSerializer(stores, many=False)
        store_merchant_id = store_serialize.data['merchant']

        # selected store does not belong to the merchant
        if int(data_merchant_id) != int(store_merchant_id):
            raise serializers.ValidationError(
                "Store Does not Belong to the Merchant")

        return store

    def validate_items(self, items):
        query_dict = QueryDict('', mutable=True)
        query_dict.update(self.initial_data)
        self.initial_data = query_dict

        data_merchant_id = int(self.initial_data.get('merchant', default=None))
        data_items_id = self.initial_data.getlist('items', default=[])

        items = Item.objects.filter(pk__in=data_items_id).all()
        serialized_items = ItemSerializer(items, many=True)

        # to check if all the items send in order details belong to the same merchant
        for item in serialized_items.data:
            if (int(item['merchant']) != data_merchant_id):
                raise serializers.ValidationError(
                    "Items Does not Belong to the Store,Merchant")

        return items
