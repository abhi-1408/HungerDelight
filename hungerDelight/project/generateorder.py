from .celery import app
from rest_framework.test import APIClient
from django.urls import reverse, resolve
from django.contrib.auth.models import User


@app.task
def generate_order(i):
    admin_user = User.objects.filter(
        username='abhi').first()
    # print('admin user is', admin_user.password)
    client = APIClient()
    client.force_authenticate(user=admin_user)
    payment_mode = ['CARD', 'CASH', 'WALLET']
    merchant_id = 2 if i % 2 == 0 else 13
    # print('merchant id is', merchant_id)
    store_map_merchant = {
        '2': [1, 3],
        '13': [6]
    }
    store = store_map_merchant.get(str(merchant_id))
    store_id = store[i % len(store)]
    # print('store arr', store, ' store id', store_id)
    item_map_merchant = {
        '2': [2, 3],
        '13': [5]
    }
    item = item_map_merchant.get(str(merchant_id))
    item_id = item[i % len(item)]
    # print('item arr', item, ' item id ', item_id)
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
    # print('send order data', send_data_order)
    response_order = client.post(
        reverse('order-list'), data=send_data_order)
    print('response is ', response_order)
    print('RESPONSE: ', response_order.status_code)


def run(n):
    for i in range(n):
        generate_order.delay(i)
