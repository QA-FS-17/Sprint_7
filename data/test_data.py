# test_data.py

import random
import string
from datetime import datetime, timedelta


class TestData:
    # Базовые URL
    BASE_URL = "https://qa-scooter.praktikum-services.ru"

    # Новые константы для сообщений API
    NOT_FOUND_MESSAGE = "Not Found."
    INSUFFICIENT_DATA_MESSAGE = "Недостаточно данных"
    COURIER_NOT_FOUND_MESSAGE = "Курьера с таким id нет"
    COURIER_NOT_EXIST_MESSAGE = "Курьера с таким id не существует"
    ORDER_NOT_FOUND_MESSAGE = "Заказ не найден"
    ORDER_NOT_EXIST_MESSAGE = "Заказа с таким id не существует"
    ORDER_ALREADY_ACCEPTED_MESSAGE = "Этот заказ уже в работе"
    LOGIN_ALREADY_USED_MESSAGE = "Этот логин уже используется"
    VALID_COLORS = ["BLACK", "GREY"]


    @staticmethod
    def generate_random_string(length):
        """Генерирует случайную строку из букв нижнего регистра"""
        return ''.join(random.choices(string.ascii_lowercase, k=length))

    @staticmethod
    def generate_courier_data():
        """Генерирует данные курьера"""
        return {
            "login": f"courier_{TestData.generate_random_string(8)}",
            "password": TestData.generate_random_string(10),
            "firstName": TestData.generate_random_string(10)
        }

    # Модифицированный метод generate_order_data (гибридный вариант)
    @staticmethod
    def generate_order_data(color=None):
        """Генерирует данные заказа с динамическими значениями"""
        return {
            "firstName": TestData.generate_random_string(10),
            "lastName": TestData.generate_random_string(10),
            "address": f"г. {TestData.generate_random_string(5)}, ул. {TestData.generate_random_string(8)}, {random.randint(1, 100)}",
            "metroStation": random.randint(1, 10),
            "phone": f"+7{random.randint(9000000000, 9999999999)}",
            "rentTime": random.randint(1, 7),
            "deliveryDate": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
            "comment": TestData.generate_random_string(20),
            **({"color": color} if color else {})
        }