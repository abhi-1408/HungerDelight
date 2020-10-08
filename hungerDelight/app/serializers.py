from rest_framework import serializers
from .models import Merchant, Store, Item, Order
from silk.profiling.profiler import silk_profile


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
    To display all fields in request, whereas for form need to display only certain fields
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

    def create(self, validated_data):
        '''
            performing calculation for total price, total items before saving
        '''

        log.msg('Create Order Request', req=self)

        item_set = validated_data.pop('items', [])
        # calculating the total items & total price form the item set sent in payload
        total_items = len(item_set)
        total_price = 0.0
        for item in item_set:
            total_price += float(item.price)

        validated_data['total_items'] = total_items
        validated_data['total_amount'] = total_price

        # creating the order
        order = Order.objects.create(**validated_data)
        for item in item_set:
            order.items.add(item)
        order.save()

        return order

    @silk_profile(name='validate-items-store')
    def validate(self, data):
        '''
            to validate the payload:
                - all items belong to the same merchant
                - store also belong to the same merchant
        '''
        merchant_id = data['merchant'].id

        data_store_merchant_id = data['store'].merchant.id
        # if the store belongs to the merchant that was sent in the data
        if int(data_store_merchant_id) != int(merchant_id):
            raise serializers.ValidationError(
                "Store Does not Belong to the Merchant")

        items_id = []
        for item in data['items']:
            items_id.append(item.id)

        items_with_merchant = Item.objects.filter(
            id__in=items_id).select_related('merchant').all()

        # if all the items belong to the same merchant
        for item in items_with_merchant:
            if int(item.merchant.id) != int(merchant_id):
                raise serializers.ValidationError(
                    "Item Does not Belong to the Merchant")

        return data
