# test_additional.py

import allure
import pytest
import requests
from data.test_data import TestData


@allure.epic("API Яндекс.Самокат")
@allure.feature("Дополнительные сценарии")
class TestAdditional:
    @allure.story("Удаление курьера")
    @allure.title("Успешное удаление курьера")
    def test_delete_courier_success(self, courier_api, created_courier):
        with allure.step("Получить ID курьера"):
            login = courier_api.login_courier(**created_courier)
            courier_id = login.json()["id"]

        with allure.step("Отправить запрос на удаление"):
            response = courier_api.delete_courier(courier_id)

        with allure.step("Проверить ответ"):
            assert response.status_code == 200
            assert response.json() == {"ok": True}

    @allure.story("Удаление курьера")
    @allure.title("Попытка удаления несуществующего курьера")
    def test_delete_nonexistent_courier_fails(self, courier_api):
        with allure.step("Отправить запрос с несуществующим ID"):
            response = courier_api.delete_courier(999999)

        assert response.status_code == 404
        assert "Курьера с таким id нет" in response.json()["message"]

    @allure.story("Принятие заказа")
    @allure.title("Успешное принятие заказа")
    def test_accept_order_success(self, courier_api, order_api, created_courier, created_order):
        with allure.step("Получить ID курьера"):
            login = courier_api.login_courier(**created_courier)
            courier_id = login.json()["id"]

        with allure.step("Получить ID заказа"):
            order_info = order_api.get_order_by_track(created_order).json()
            order_id = order_info["order"]["id"]

        with allure.step("Принять заказ"):
            response = order_api.accept_order(order_id, courier_id)

        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.story("Принятие заказа")
    @allure.title("Попытка принять заказ без обязательного параметра: {missing_param}")
    @pytest.mark.parametrize("missing_param", ["courierId", "orderId"])
    def test_accept_order_missing_param(self, courier_api, order_api, created_courier, created_order, missing_param):
        with allure.step("Подготовить данные"):
            login = courier_api.login_courier(**created_courier)
            courier_id = login.json()["id"]
            order_id = order_api.get_order_by_track(created_order).json()["order"]["id"]

        with allure.step("Отправить запрос без параметра"):
            if missing_param == "courierId":
                url = f"{TestData.BASE_URL}/api/v1/orders/accept/{order_id}"
            else:
                url = f"{TestData.BASE_URL}/api/v1/orders/accept/?courierId={courier_id}"

            response = requests.put(url)

        assert response.status_code == 400
        assert "Недостаточно данных" in response.json()["message"]

    @allure.story("Получение заказа")
    @allure.title("Успешное получение заказа по треку")
    def test_get_order_by_track_success(self, order_api, created_order):
        with allure.step("Запросить заказ по треку"):
            response = order_api.get_order_by_track(created_order)

        assert response.status_code == 200
        assert "order" in response.json()

    @allure.story("Получение заказа")
    @allure.title("Попытка получить заказ без трека")
    def test_get_order_without_track(self):
        with allure.step("Отправить запрос без параметра track"):
            response = requests.get(f"{TestData.BASE_URL}/api/v1/orders/track")

        assert response.status_code == 400
        assert "Недостаточно данных" in response.json()["message"]

    @allure.story("Получение заказа")
    @allure.title("Попытка получить несуществующий заказ")
    def test_get_nonexistent_order_fails(self, order_api):
        with allure.step("Отправить запрос с несуществующим треком"):
            response = order_api.get_order_by_track(999999)

        assert response.status_code == 404
        assert "Заказ не найден" in response.json()["message"]