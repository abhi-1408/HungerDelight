import pytest
from django.urls import reverse, resolve
from django.conf import settings
from app.models import Merchant, Item, Store, Order
from app.views import MerchantViewSet
# Create your tests here.
from django.contrib.auth.models import User
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from mixer.backend.django import mixer


class TestCrud:
    @pytest.fixture
    def client(self, admin_user):
        client = APIClient()
        client.force_authenticate(user=admin_user)
        return client

    @pytest.fixture
    def merchant(self, db):
        merchant = Merchant(
            name="Haldiram", email="haldiram@gmail.com", mobile="9988990909")
        merchant.save()

        # merchant = mixer.blend('app.Merchant')
        return merchant

    @pytest.fixture
    def item(self, db, merchant):
        item = Item(
            name="Doda Barfi",
            price="700.000000",
            description="Fresh Desi Ghee Made",
            merchant=merchant
        )
        item.save()
        # merchant = mixer.blend('app.Item')
        return item

    @pytest.fixture
    def store(self, db, merchant, item):
        store = Store(
            name="Mumbai BB",
            address="Worli, Mumbai",
            lat="65.450000000000000",
            lng="34.550000000000000",
            operational=True,
            merchant=merchant,
            items=[item]
        )
        store.save()
        # store = mixer.blend('app.Store')
        return store

    @ pytest.mark.django_db
    def test_merchant_list(self, client, merchant):

        response = client.get(reverse('merchant-list'))

        data = response.json()
        assert [{"id": data[0]['id'],
                 "name": "Haldiram",
                 "email": "haldiram@gmail.com",
                 "mobile": "9988990909"}] == data

    @ pytest.mark.django_db
    def test_item_list(self, client, item, merchant):

        response = client.get(reverse('item-list'))
        data = response.json()
        assert [{
            "id": data[0]['id'],
            "name": "Doda Barfi",
            "price": "700.000000",
            "created_at": data[0]['created_at'],
            "description": "Fresh Desi Ghee Made",
            "merchant": data[0]['merchant']
        }] == data

    # @ pytest.mark.django_db
    # def test_store_creation(self, client, store):

    #     response = client.get(reverse('store-list'))

    #     data = response.json()
    #     print('STORE IS', data)
    #     assert [{
    #             "id": 1,
    #             "name": "Mumbai BB",
    #             "address": "Worli, Mumbai",
    #             "lat": "65.450000000000000",
    #             "lng": "34.550000000000000",
    #             "operational": True,
    #             "merchant": 1,
    #             "items": [1]
    #             }] == data
