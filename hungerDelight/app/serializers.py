from rest_framework import serializers
from .models import Merchant, Store, Item, Order


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
        data_store_id = int(self.initial_data['store'])
        data_merchant_id = int(self.initial_data['merchant'])
        stores = Store.objects.get(id=data_store_id)
        store_serialize = StoreSerializer(stores, many=False)
        store_merchant_id = store_serialize.data['merchant']

        # selected store belongs to the merchant
        if data_merchant_id == store_merchant_id:
            return store
        else:
            # selected store does not belong to the merchant
            raise serializers.ValidationError(
                "Store Does not Belong to the Merchant")
