from __future__ import absolute_import

from celery import shared_task
from rest_framework.test import APIClient
from django.urls import reverse, resolve
from django.contrib.auth.models import User


@shared_task
def generate_order(i):
    admin_user = User.objects.filter(
        username='abhi').first()

    client = APIClient()
    client.force_authenticate(user=admin_user)
    payment_mode = ['CARD', 'CASH', 'WALLET']
    merchant_id = 2 if i % 2 == 0 else 13

    store_map_merchant = {
        '2': [1, 3],
        '13': [6]
    }
    store = store_map_merchant.get(str(merchant_id))
    store_id = store[i % len(store)]

    item_map_merchant = {
        '2': [2, 3],
        '13': [5]
    }
    item = item_map_merchant.get(str(merchant_id))
    item_id = item[i % len(item)]

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
