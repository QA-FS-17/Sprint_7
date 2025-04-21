# courier_api.py

import allure
import requests
import logging
from data.test_data import TestData

logger = logging.getLogger(__name__)


class CourierApi:
    def __init__(self):
        self.base_url = TestData.BASE_URL

    @allure.step("Создать курьера (логин: {login})")
    def create_courier(self, login=None, password=None, firstName=None):
        """Создание курьера с указанными данными"""
        payload = {
            "login": login,
            "password": password,
            "firstName": firstName
        }

        # Фильтруем None-значения
        payload = {k: v for k, v in payload.items() if v is not None}

        logger.info(f"Создание курьера с данными: {payload}")
        response = requests.post(
            f"{self.base_url}/api/v1/courier",
            json=payload
        )
        logger.info(f"Результат создания курьера. Статус: {response.status_code}, Ответ: {response.text}")
        return response

    @allure.step("Авторизовать курьера (логин: {login})")
    def login_courier(self, login, password):
        """Авторизация курьера"""
        payload = {
            "login": login,
            "password": password
        }

        logger.info(f"Авторизация курьера: {login}")
        response = requests.post(
            f"{self.base_url}/api/v1/courier/login",
            data=payload
        )
        logger.info(f"Результат авторизации. Статус: {response.status_code}, Ответ: {response.text}")
        return response

    @allure.step("Удалить курьера (ID: {courier_id})")
    def delete_courier(self, courier_id):
        """Удаление курьера по ID"""
        logger.info(f"Удаление курьера с ID: {courier_id}")
        response = requests.delete(f"{self.base_url}/api/v1/courier/{courier_id}")
        logger.info(f"Результат удаления. Статус: {response.status_code}, Ответ: {response.text}")
        return response