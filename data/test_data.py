# test_data.py

import allure
import random
import string

class TestData:
    BASE_URL = "https://qa-scooter.praktikum-services.ru"

    @staticmethod
    def generate_random_string(length):
        """Генерирует случайную строку из букв нижнего регистра"""
        return ''.join(random.choices(string.ascii_lowercase, k=length))

    @staticmethod
    def generate_courier_data():
        """Генерирует данные курьера"""
        return {
            "login": TestData.generate_random_string(10),
            "password": TestData.generate_random_string(10),
            "firstName": TestData.generate_random_string(10)
        }

    @staticmethod
    @allure.step("Сгенерировать данные заказа")
    def generate_order_data(color=None):
        """Генерирует данные заказа"""
        payload = {
            "firstName": "TestUser",
            "lastName": "TestLastName",
            "address": "Moscow, Test st. 42",
            "metroStation": 4,
            "phone": "+7" + ''.join(random.choices(string.digits, k=10)),
            "rentTime": 5,
            "deliveryDate": "2024-12-31",
            "comment": "Standard test order"
        }
        if color:
            payload["color"] = color
        return payload