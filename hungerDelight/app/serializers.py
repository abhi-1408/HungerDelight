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
    # days_since_joined = serializers.SerializerMethodField(
    #     'get_days_since_joined')

    class Meta:
        model = Order
        fields = '__all__'
        # fields = ('timeStamp', 'status', 'paymentMode',
        #           'store', 'merchant', 'items')


class OrderSerializer(serializers.ModelSerializer):
    # days_since_joined = serializers.SerializerMethodField(
    #     'get_days_since_joined')

    class Meta:
        model = Order
        # fields = '__all__'
        fields = ('timestamp', 'status', 'payment_mode',
                  'store', 'merchant', 'items')

    # def get_days_since_joined(self, obj):
    #     return (10 + obj.totalAmount)

    def create(self, validated_data):
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

        if data_store_id != None and data_merchant_id != None:
            stores = Store.objects.filter(id=data_store_id).first()

            if stores == None:
                raise serializers.ValidationError(
                    "Store Not Present")

            store_serialize = StoreSerializer(stores, many=False)
            store_merchant_id = store_serialize.data['merchant']

            # selected store does not belong to the merchant
            if data_merchant_id != store_merchant_id:
                raise serializers.ValidationError(
                    "Store Does not Belong to the Merchant")

            return store
        raise serializers.ValidationError(
            "Please select a merchant and store")

    # def validate_total_items(self, total_items):
    #     '''
    #     Checks if the total items count is equal to the items selected
    #     '''
    #     items_count = len(self.initial_data.getlist('items', default=[]))
    #     if total_items != items_count:
    #         raise serializers.ValidationError(
    #             "Total Items Count & Items Selected Count do not match, Please Check")

    #     return total_items
