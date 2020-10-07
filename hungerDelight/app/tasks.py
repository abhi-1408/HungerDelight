from __future__ import absolute_import

from celery import shared_task
from rest_framework.test import APIClient
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from .models import Merchant, Item, Store, Order
from .serializers import MerchantSerializer, ItemSerializer, StoreSerializer, OrderSerializer
from datetime import datetime
import structlog
logger = structlog.get_logger()


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


@shared_task
def create_order(validated_data):
    # print('got data as in async', order_data)
    log = logger.bind(task='Async Create Order Request', data=validated_data)
    # print('request data in celery', validated_data)
    store_id = validated_data['store']
    merchant_id = validated_data['merchant']
    item_id = validated_data['items']
    timestamp = datetime.now(
    ) if validated_data.get('timestamp') == '' or validated_data.get('timestamp') == None else validated_data.get('timestamp')

    merchant = Merchant.objects.filter(id=merchant_id).first()
    store = Store.objects.filter(id=store_id).first()

    items_list = Item.objects.filter(id__in=item_id).all()
    total_items = items_list.count()
    total_price = 0.0
    for item in items_list:
        total_price += float(item.price)

    order = Order.objects.create(
        timestamp=timestamp, payment_mode=validated_data['payment_mode'], store=store, merchant=merchant, status=validated_data['status'], total_amount=total_price, total_items=total_items)
    for item in items_list:
        order.items.add(item)
    order.save()
    log.msg('success', task='order created successfully')
    # print('order created')
