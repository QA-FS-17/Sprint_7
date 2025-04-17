# conftest.py

import pytest
import allure
from api.courier_api import CourierApi
from api.order_api import OrderApi
from data.test_data import TestData


@pytest.fixture
def courier_api():
    """Базовый клиент API для работы с курьерами"""
    return CourierApi()


@pytest.fixture
def order_api():
    """Базовый клиент API для работы с заказами"""
    return OrderApi()


@pytest.fixture
def courier_data():
    """Генерирует тестовые данные курьера"""
    return TestData.generate_courier_data()


@pytest.fixture(scope="class")
def class_courier(courier_api, courier_data):
    """Курьер для тестов класса (создаётся один раз)"""
    with allure.step("Создание курьера для тестов класса"):
        response = courier_api.create_courier(**courier_data)
        assert response.status_code == 201

    yield {"api": courier_api, "data": courier_data}

    with allure.step("Удаление курьера класса"):
        login = courier_api.login_courier(login=courier_data["login"], password=courier_data["password"])
        if login.status_code == 200:
            courier_api.delete_courier(login.json()["id"])


@pytest.fixture
def function_courier(courier_api, courier_data):
    """Курьер для отдельных тестовых функций"""
    with allure.step("Создание временного курьера"):
        response = courier_api.create_courier(**courier_data)
        assert response.status_code == 201

    yield courier_data

    with allure.step("Удаление временного курьера"):
        login = courier_api.login_courier(login=courier_data["login"], password=courier_data["password"])
        if login.status_code == 200:
            courier_api.delete_courier(login.json()["id"])


@pytest.fixture
def created_order(order_api):
    """Фикстура создания тестового заказа"""
    with allure.step("Создание тестового заказа"):
        response = order_api.create_order(TestData.generate_order_data())
        assert response.status_code == 201
        yield response.json()["track"]