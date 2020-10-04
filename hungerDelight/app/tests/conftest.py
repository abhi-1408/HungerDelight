import pytest
from rest_framework.test import APIClient
from app.models import Merchant, Item, Store, Order
from django.contrib.auth.models import User


@pytest.fixture(scope='module')
def django_db_setup(request, django_db_setup):
    print('executing*******')
    pass


@pytest.fixture
def client(admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client

# @pytest.fixture(scope='session')
# def client(django_db_setup, django_db_blocker):
#     with django_db_blocker.unblock():
#         client = APIClient()
#         user = User.objects.create_user(
#             username='admin', password='admin')
#         client.force_authenticate(user=user)
#         yield client

#     with django_db_blocker.unblock():
#         client.force_authenticate(user=None)


@pytest.fixture(scope='module')
def merchant(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():

        print('FIXTURE CREATED')
        for i in range(2):
            merchant = Merchant(
                name=f"name{i+1}", email=f"merc{i+1}@gmail.com", mobile="9999999999")
            merchant.save()

        merchant = Merchant.objects.all()
        # merchant = mixer.blend('app.Merchant')
        yield merchant

    # deleting the merchant after test suite run completed,
    # deleting merchant would also delete all other entries as it ondelete.CASCADE in other tables
    with django_db_blocker.unblock():
        print('deleting')
        merchant.delete()


@pytest.fixture(scope='module')
def item(django_db_setup, django_db_blocker, merchant):
    with django_db_blocker.unblock():
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


@pytest.fixture(scope='module')
def store(django_db_setup, django_db_blocker, merchant, item):
    with django_db_blocker.unblock():
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


@pytest.fixture(scope='module')
def order(django_db_setup, django_db_blocker, merchant, item, store):
    with django_db_blocker.unblock():
        order = Order.objects.create(
            total_amount='100.000000',
            total_items="1",
            timestamp="2020-09-30T17:19:00Z",
            status="SUCCESS",
            payment_mode="CASH",
            store=store,
            merchant=merchant[0],


        )
        order.items.add(item[0])
        order.save()
        # store = mixer.blend('app.Store')
        return order


# @pytest.fixture(scope='session')
# def django_db_modify_db_settings():
#     pass
