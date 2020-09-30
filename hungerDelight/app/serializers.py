from rest_framework import serializers
from .models import Merchant, Store, Item, Order
import json


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


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def validate_store(self, store):
        '''
        Checks if the store selected belong to the merchant or not

        '''
        initial_data_dict = dict(self.initial_data)
        data_store_id = int(initial_data_dict['store'][0])
        data_merchant_id = int(initial_data_dict['merchant'][0])
        stores = Store.objects.get(id=data_store_id)
        store_serialize = StoreSerializer(stores, many=False)
        store_merchant_id = store_serialize.data['merchant']

        # selected store does not belong to the merchant
        if data_merchant_id != store_merchant_id:
            raise serializers.ValidationError(
                "Store Does not Belong to the Merchant")

        return store

    def validate_total_items(self, total_items):
        '''
        Checks if the total items count is equal to the items selected
        '''
        initial_data_dict = dict(self.initial_data)
        items_count = len(initial_data_dict['items'])

        if total_items != items_count:
            raise serializers.ValidationError(
                "Total Items Count & Items Selected Count do not match, Please Check")

        return total_items
