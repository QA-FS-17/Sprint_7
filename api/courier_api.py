# courier_api.py

import allure
import requests
from data.test_data import TestData

class CourierApi:
    def __init__(self):
        self.base_url = TestData.BASE_URL

    @allure.step("Создать курьера (логин: {login})")
    def create_courier(self, login, password, first_name):
        """Создание курьера с указанными данными"""
        return requests.post(
            f"{self.base_url}/api/v1/courier",
            data={
                "login": login,
                "password": password,
                "firstName": first_name
            }
        )

    @allure.step("Авторизовать курьера (логин: {login})")
    def login_courier(self, login, password):
        """Авторизация курьера"""
        return requests.post(
            f"{self.base_url}/api/v1/courier/login",
            data={
                "login": login,
                "password": password
            }
        )

    @allure.step("Удалить курьера (ID: {courier_id})")
    def delete_courier(self, courier_id):
        """Удаление курьера по ID"""
        return requests.delete(f"{self.base_url}/api/v1/courier/{courier_id}")