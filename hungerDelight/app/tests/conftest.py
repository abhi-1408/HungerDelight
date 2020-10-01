import pytest
from rest_framework.test import APIClient
from app.models import Merchant, Item, Store, Order


@pytest.fixture
def client(admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client


@pytest.fixture
def merchant(db):
    for i in range(2):
        merchant = Merchant(
            name=f"name{i+1}", email=f"merc{i+1}@gmail.com", mobile="9999999999")
        merchant.save()

    merchant = Merchant.objects.all()
    # merchant = mixer.blend('app.Merchant')
    return merchant


@pytest.fixture
def item(db, merchant):
    for i in range(3):

        item = Item(
            name=f"item{i+1}",
            price=f"{i+1}00",
            description=f"desc{i+1}",
            merchant=merchant[i % 2]
        )
        item.save()
    item = Item.objects.all()
    # merchant = mixer.blend('app.Merchant')
    return item


@pytest.fixture
def store(db, merchant, item):
    store = Store.objects.create(
        name="Mumbai BB",
        address="Worli, Mumbai",
        lat="65.450000000000000",
        lng="34.550000000000000",
        operational=True,
        merchant=merchant[0],

    )
    store.items.add(item[0])
    store.items.add(item[2])
    store.save()
    # store = mixer.blend('app.Store')
    return store


@pytest.fixture
def order(db, merchant, item, store):
    order = Order.objects.create(
        totalAmount="100.00",
        total_items="2",
        timeStamp="2020-09-30T17:19:00Z",
        status="SUCCESS",
        paymentMode="CASH",
        store=store,
        merchant=merchant[0],


    )
    order.items.add(item[0])
    order.save()
    # store = mixer.blend('app.Store')
    return order


@pytest.fixture(scope='session')
def django_db_modify_db_settings():
    pass
