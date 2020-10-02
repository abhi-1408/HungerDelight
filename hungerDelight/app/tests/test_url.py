import pytest
from django.urls import reverse, resolve
from django.conf import settings
from app.models import Merchant, Item, Store, Order
from app.serializers import MerchantSerializer, ItemSerializer, StoreSerializer
from app.views import MerchantViewSet
# Create your tests here.
from django.contrib.auth.models import User
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from mixer.backend.django import mixer


class TestCrud:
    @ pytest.mark.django_db
    def test_merchant_list(self, client, merchant):

        response = client.get(reverse('merchant-list'))

        data = response.json()
        assert [{"id": data[0]['id'],
                 "name": "name1",
                 "email": "merc1@gmail.com",
                 "mobile": "9999999999"}, {"id": data[1]['id'],
                                           "name": "name2",
                                           "email": "merc2@gmail.com",
                                           "mobile": "9999999999"}] == data

    @ pytest.mark.django_db
    def test_item_list(self, client, item, merchant):

        response = client.get(reverse('item-list'))
        data = response.json()
        assert [{
            "id": data[0]['id'],
            "name": "item1",
            "price": "100.000000",
            "created_at": data[0]['created_at'],
            "description": "desc1",
            "merchant": data[0]['merchant']
        }, {
            "id": data[1]['id'],
            "name": "item2",
            "price": "200.000000",
            "created_at": data[1]['created_at'],
            "description": "desc2",
            "merchant": data[1]['merchant']
        }, {
            "id": data[2]['id'],
            "name": "item3",
            "price": "300.000000",
            "created_at": data[2]['created_at'],
            "description": "desc3",
            "merchant": data[2]['merchant']
        }] == data

    @ pytest.mark.django_db
    def test_store_list(self, client, store):

        response = client.get(reverse('store-list'))

        data = response.json()
        assert [{
                "id": data[0]['id'],
                "name": "Mumbai BB",
                "address": "Worli, Mumbai",
                "lat": "65.450000000000000",
                "lng": "34.550000000000000",
                "operational": True,
                "merchant": data[0]['merchant'],
                "items": data[0]['items']
                }] == data

    @ pytest.mark.django_db
    def test_order_list(self, client, order):

        response = client.get(reverse('order-list'))

        data = response.json()
        assert [{
                "id": data[0]['id'],
                "total_items":1,
                "total_amount":'100.000000',
                "timestamp": data[0]['timestamp'],
                "status": "SUCCESS",
                "payment_mode": "CASH",
                "store": data[0]['store'],
                "merchant": data[0]['merchant'],
                "items": data[0]['items']
                }] == data

    @ pytest.mark.django_db
    def test_order_creation_api(self, client, store, merchant, item):
        store_serial = StoreSerializer(store, many=False)
        merchant_serial = MerchantSerializer(merchant, many=True)
        item_serial = ItemSerializer(item, many=True)
        send_data = {
            "timestamp": "2020-10-01T22:10:00Z",
            "status": "SUCCESS",
            "payment_mode": "CARD",
            "store": store_serial.data['id'],
            "merchant": merchant_serial.data[0]['id'],
            "items": [
                item_serial.data[0]['id']
            ],

        }
        response = client.post(reverse('order-list'), data=send_data)
        assert response.status_code == 201
