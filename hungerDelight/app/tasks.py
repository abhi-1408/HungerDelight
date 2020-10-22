from celery import states
import json
import requests
from celery import shared_task
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Merchant, Item, Store, Order
from .serializers import MerchantSerializer, ItemSerializer, StoreSerializer, OrderSerializer
from datetime import datetime
import structlog
from project.celery import app
logger = structlog.get_logger()


@shared_task
def generate_order(i):
    '''
        generate n random orders

    '''
    admin_user = User.objects.filter(
        username='admin').first()

    client = APIClient()
    client.force_authenticate(user=admin_user)
    payment_mode = ['CARD', 'CASH', 'WALLET']

    # fetch a random merchant id
    all_merchant = Merchant.objects.all()
    merchant_ind = i % all_merchant.count()
    merchant_id = all_merchant[merchant_ind].id

    #  fetch a random store belonging to the selected merchant
    all_store = Store.objects.filter(merchant=merchant_id).all()
    if all_store.count() == 0:
        return
    store_ind = i % all_store.count()
    store_id = all_store[store_ind].id

    # fetch a random item belonging to the selected merchant
    all_item = Item.objects.filter(merchant=merchant_id).all()
    if all_item.count() == 0:
        return
    item_ind = i % all_item.count()
    item_id = all_item[item_ind].id

    print('merchant id', merchant_id, ' store id',
          store_id, ' item id', item_id)
    # create the send order data
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


@app.task(bind=True, autoretry_for=(Exception,), max_retries=5, default_retry_delay=20)
def create_order(self, validated_data):
    '''
        async order creation, it fetches from the queue for any order related data,
            if there is a data in queue, it creates the order for it in the models.

    '''
    log = logger.bind(task='Async Create Order Request', data=validated_data)

    # get the store, merchant, and items from the data
    store_id = validated_data['store']
    merchant_id = validated_data['merchant']
    item_id = validated_data['items']

    # add a datetime if not given in validated_data
    timestamp = datetime.now(
    ) if validated_data.get('timestamp') == '' or validated_data.get('timestamp') == None else validated_data.get('timestamp')

    # fetch the merchant and store object
    merchant = Merchant.objects.filter(id=merchant_id).first()
    store = Store.objects.filter(id=store_id).first()

    #  fetch all the item objects
    items_list = Item.objects.filter(id__in=item_id).all()
    total_items = items_list.count()
    total_price = 0.0
    for item in items_list:
        total_price += float(item.price)

    # create a object of the order data collected above
    order = Order.objects.create(
        timestamp=timestamp, payment_mode=validated_data['payment_mode'], store=store, merchant=merchant, status=validated_data['status'], total_amount=total_price, total_items=total_items)
    for item in items_list:
        order.items.add(item)
    order.save()
    log.msg('success', task='order created successfully')

    serial_order = OrderSerializer(order)
    return serial_order.data


@app.task(bind=True)
def webhook(self, order_data):

    logger.msg('webook request sent', order_data=order_data)
    res = requests.post('http://localhost:8000/app/webhook/',
                        json=order_data)

    # if res.status_code == 400:
    #     self.update_state(state=states.FAILURE)
    # print(dir(self))
    return res


@app.task(bind=True)
def myerror(self, uuid):
    logger.msg('webook request failed', uuid=uuid)
    return
