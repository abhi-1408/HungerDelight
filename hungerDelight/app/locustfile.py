import time
from locust import HttpUser, task, between


class QuickstartUser(HttpUser):
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

    # @task
    # def order_page(self):
    #     self.client.post("/app/order/",
    #                      auth=("admin", "admin"),
    #                      json={
    #                          "timestamp": "2020-10-07T06:27:15.381619Z",
    #                          "status": "AWAITING",
    #                          "payment_mode": "CASH",
    #                          "store": 1,
    #                          "merchant": 2,
    #                          "items": [
    #                              3
    #                          ]})
