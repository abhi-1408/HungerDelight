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

    def validate_total_items(self, total_items):
        '''
        Checks if the total items count is equal to the items selected
        '''
        items_count = len(self.initial_data.getlist('items', default=[]))
        if total_items != items_count:
            raise serializers.ValidationError(
                "Total Items Count & Items Selected Count do not match, Please Check")

        return total_items
