import pytest
from django.urls import reverse
from app.models import Merchant, Item, Store, Order
from app.serializers import MerchantSerializer, ItemSerializer, StoreSerializer
from app.views import MerchantViewSet
# Create your tests here.


class TestCrud:
    @ pytest.mark.django_db
    def test_merchant_list(self, client, merchant):
        '''
            To test as the merchants created and the merchants fetched are same or not
        '''
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
        '''
            to check the items created and the items data shown in list view is correct or not
        '''
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
        '''
             to check the stores created and the stores data shown in list view is correct or not
        '''
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
        '''
         to check the orders created and the orders data shown in list view is correct or not
        '''
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
        '''
            to check that is a order created successfully by using a post request.
        '''
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
        response = client.post(reverse('order-list'),
                               data=send_data, format='json')
        assert response.status_code == 201


class TestApi:
    @ pytest.mark.django_db
    @ pytest.mark.parametrize('send_data', [({
        "timestamp": "2020-10-01T22:10:00Z",
        "status": "SUCCESS",
        "payment_mode": "CARD",
        "store": 1,
        "merchant": 2
    }), ({
        "timestamp": "2020-10-01T22:10:00Z",
        "status": "SUCCESS",
        "payment_mode": "CARD",
        "merchant": 2,

    }), ({
        "timestamp": "2020-10-01T22:10:00Z",
        "status": "SUCCESS",
        "payment_mode": "CARD",
        "items": [
            2, 3
        ],

    }),
    ])
    def test_bad_order_creation_request(self, send_data, client):
        '''
            to test the if wrong/bad payload is sent for order creation, it should give a HTTP_400
        '''
        response = client.post(reverse('order-list'), data=send_data)
        assert response.status_code == 400

    @ pytest.mark.django_db
    @ pytest.mark.parametrize('send_data_merchant,send_data_item,send_data_store,send_data_order,status_code', [
        ({

            "name": "merchap1",
            "email": "mercapi1@gmail.com",
            "mobile": "9988998899"
        }, {

            "name": "Doda Barfi",
            "price": "700.000000",
            "created_at": "2020-09-30T11:46:05.547188Z",
            "description": "Fresh Desi Ghee Made",
            "merchant": 1
        }, {

            "name": "Delhi BB",
            "address": "Patparganj, New Delhi",
            "lat": "45.560000000000000",
            "lng": "98.440000000000000",
            "operational": True,
            "merchant": 1,
            "items": [
                1
            ]
        },
            {
                "timestamp": "2020-10-01T22:10:00Z",
                "status": "SUCCESS",
                "payment_mode": "CARD",
                "store": 1,
                "merchant": 1,
                "items": [
                    1
                ]

        },
            201),
    ])
    def test_order_creation_cycle_request(self, send_data_merchant, send_data_item, send_data_store, send_data_order, status_code, client):
        '''
            to test the full order creation cycle:
                1. a merchant created through post request
                2. a item is created and attached with the merchant through post request
                3. a store is created and is attched with the merchant through post request
                4. a order is created for the specific merchant, item a& store.
        '''
        # merchant is created
        response_merchant = client.post(reverse('merchant-list'),
                                        data=send_data_merchant)

        # merchant response is used to add merchant_id in the item creation nrequest
        send_data_item['merchant'] = response_merchant.data['id']
        response_item = client.post(
            reverse('item-list'), data=send_data_item)

        #  merchant_id are used in the store creation request
        send_data_store['merchant'] = response_merchant.data['id']
        response_store = client.post(
            reverse('store-list'), data=send_data_store)

        # merchant_id, item_id and store_id from previous responses are used in the order creation request
        send_data_order['merchant'] = response_merchant.data['id']
        send_data_order['items'] = [response_item.data['id']]
        send_data_order['store'] = response_store.data['id']
        response_order = client.post(
            reverse('order-list'), data=send_data_order)

        assert response_order.status_code == status_code
