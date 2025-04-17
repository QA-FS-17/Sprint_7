# order_api.py

import allure
import requests
from data.test_data import TestData

class OrderApi:
    def __init__(self):
        self.base_url = TestData.BASE_URL

    @allure.step("Создать заказ (цвет: {payload.get('color', 'без цвета')}")
    def create_order(self, payload):
        return requests.post(f"{self.base_url}/api/v1/orders", json=payload)

    @allure.step("Получить список заказов")
    def get_orders_list(self):
        return requests.get(f"{self.base_url}/api/v1/orders")

    @allure.step("Получить заказ по треку №{track}")
    def get_order_by_track(self, track):
        return requests.get(f"{self.base_url}/api/v1/orders/track?t={track}")

    @allure.step("Принять заказ №{order_id} курьером {courier_id}")
    def accept_order(self, order_id, courier_id):
        return requests.put(f"{self.base_url}/api/v1/orders/accept/{order_id}?courierId={courier_id}")