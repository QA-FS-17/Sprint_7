# test_data.py

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
    def generate_order_data(color=None):
        """Генерирует данные заказа с указанным цветом"""
        payload = {
            "firstName": "Тест",
            "lastName": "Тестов",
            "address": "Москва, ул. Тестовая, 1",
            "metroStation": 1,
            "phone": "+79999999999",
            "rentTime": 1,
            "deliveryDate": "2024-01-01",
            "comment": "Тестовый заказ"
        }
        if color:
            payload["color"] = color
        return payload