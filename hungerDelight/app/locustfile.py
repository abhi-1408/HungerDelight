import time
from locust import HttpUser, task, between


class QuickstartUser(HttpUser):
    '''
    Locust task file, to test for get request for index, merchant, store, item, order
                      to test post request for order creation

    '''
    wait_time = between(1, 2)

    @task
    def index_page(self):
        self.client.get("/app/", auth=("admin", "admin"))

    @task
    def merchant_page(self):
        self.client.get("/app/merchant/", auth=("admin", "admin"))

    @task
    def store_page(self):
        self.client.get("/app/store/", auth=("admin", "admin"))

    @task
    def item_page(self):
        self.client.get("/app/item/", auth=("admin", "admin"))

    @task
    def order_page(self):
        self.client.get("/app/order/", auth=("admin", "admin"))

    @task
    def order__creation_page(self):
        self.client.post("/app/order/",
                         auth=("admin", "admin"),
                         json={
                             "timestamp": "2020-10-07T06:27:15.381619Z",
                             "status": "SUCCESS",
                             "payment_mode": "CASH",
                             "store": 3,
                             "merchant": 2,
                             "items": [
                                 2, 6
                             ]}
                         )
