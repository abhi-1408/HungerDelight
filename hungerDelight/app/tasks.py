from __future__ import absolute_import

from celery import shared_task
from rest_framework.test import APIClient
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from .models import Merchant, Item, Store
from .serializers import MerchantSerializer, ItemSerializer, StoreSerializer


@shared_task
def generate_order(i):
    admin_user = User.objects.filter(
        username='abhi').first()

    client = APIClient()
    client.force_authenticate(user=admin_user)
    payment_mode = ['CARD', 'CASH', 'WALLET']

    all_merchant = Merchant.objects.all()
    merchant_ind = i % all_merchant.count()
    merchant_serialize = MerchantSerializer(
        all_merchant[merchant_ind], many=False)
    merchant_id = merchant_serialize.data['id']

    all_store = Store.objects.filter(merchant=merchant_id).all()
    store_ind = i % all_store.count()
    store_serialize = StoreSerializer(all_store[store_ind], many=False)
    store_id = store_serialize.data['id']

    all_item = Item.objects.filter(merchant=merchant_id).all()
    item_ind = i % all_item.count()
    item_serialize = ItemSerializer(all_item[item_ind], many=False)
    item_id = item_serialize.data['id']

    print('merchant id', merchant_id, ' store id',
          store_id, ' item id', item_id)

    send_data_order = {
        "timestamp": "2020-10-01T22:10:00Z",
        "status": "SUCCESS",
        "payment_mode": payment_mode[i % 3],
        "store": store_id,
        "merchant": merchant_id,
        "items": [
            item_id
        ]

    }
    response_order = client.post(
        reverse('order-list'), data=send_data_order)

    return response_order.status_code


def run(n):
    async_ids = []
    for i in range(n):
        id_ = generate_order.delay(i)
        async_ids.append(id_)

    return async_ids
