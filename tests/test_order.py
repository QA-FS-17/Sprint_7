# test_order.py

import allure
import pytest
from data.test_data import TestData


@allure.epic("API Яндекс.Самокат")
@allure.feature("Работа с заказами")
class TestOrder:
    @allure.story("Создание заказа")
    @allure.title("Создание заказа с цветом: {color}")
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        None
    ], ids=lambda x: str(x))
    def test_create_order_with_colors(self, order_api, color):
        with allure.step("Подготовить данные заказа"):
            payload = TestData.generate_order_data(color)

        with allure.step("Отправить запрос"):
            response = order_api.create_order(payload)

        with allure.step("Проверить ответ"):
            assert response.status_code == 201
            allure.attach(
                str(response.json()),
                name="Ответ API",
                attachment_type=allure.attachment_type.JSON
            )

    @allure.story("Получение заказов")
    @allure.title("Получить список заказов")
    def test_get_orders_list(self, order_api):
        with allure.step("Запросить список заказов"):
            response = order_api.get_orders_list()

        with allure.step("Проверить ответ"):
            assert response.status_code == 200
            orders = response.json().get("orders", [])
            allure.attach(
                f"Найдено заказов: {len(orders)}",
                name="Статистика",
                attachment_type=allure.attachment_type.TEXT
            )
            assert isinstance(orders, list)