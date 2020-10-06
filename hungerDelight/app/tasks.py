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
        username='admin').first()

    client = APIClient()
    client.force_authenticate(user=admin_user)
    payment_mode = ['CARD', 'CASH', 'WALLET']

    all_merchant = Merchant.objects.all()
    merchant_ind = i % all_merchant.count()
    merchant_id = all_merchant[merchant_ind].id

    all_store = Store.objects.filter(merchant=merchant_id).all()
    if all_store.count() == 0:
        return
    store_ind = i % all_store.count()
    store_id = all_store[store_ind].id

    all_item = Item.objects.filter(merchant=merchant_id).all()
    if all_item.count() == 0:
        return
    item_ind = i % all_item.count()
    item_id = all_item[item_ind].id

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