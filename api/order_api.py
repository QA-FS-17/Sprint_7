# order_api.py

import requests
import allure
import logging

logger = logging.getLogger(__name__)

class OrderApi:
    def __init__(self):
        self.base_url = "https://qa-scooter.praktikum-services.ru"
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    @allure.step("Создать заказ")
    def create_order(self, payload):
        url = f"{self.base_url}/api/v1/orders"
        logger.info(f"Creating order with payload: {payload}")
        response = self.session.post(url, json=payload)
        logger.info(f"Order creation response: {response.status_code} {response.text}")
        return response

    @allure.step("Отменить заказ")
    def cancel_order(self, track):
        url = f"{self.base_url}/api/v1/orders/cancel"
        logger.info(f"Cancelling order with track: {track}")
        response = self.session.put(url, json={"track": track})
        return response

    @allure.step("Получить список заказов")
    def get_orders_list(self):
        return requests.get(f"{self.base_url}/api/v1/orders")

    @allure.step("Получить заказ по треку №{track}")
    def get_order_by_track(self, track):
        return requests.get(f"{self.base_url}/api/v1/orders/track?t={track}")

    @allure.step("Принять заказ №{order_id} курьером {courier_id}")
    def accept_order(self, order_id, courier_id):
        url = f"{self.base_url}/api/v1/orders/accept/{order_id}"
        response = self.session.put(
            url,
            params={"courierId": str(courier_id)},
            headers={"Content-Type": "application/json"}
        )
        logger.info(f"Accept order response: {response.status_code} {response.text}")
        return response