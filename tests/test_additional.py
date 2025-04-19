# test_additional.py

import allure
import pytest
import requests
from data.test_data import TestData


@allure.epic("API Яндекс.Самокат")
class TestCourierDeletion:
    @allure.story("Удаление курьера")
    def test_delete_courier_success(self, courier_api, registered_courier):
        response = courier_api.delete_courier(registered_courier["id"])
        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.story("Удаление курьера")
    def test_delete_courier_missing_id(self):
        response = requests.delete(f"{TestData.BASE_URL}/api/v1/courier/")
        assert response.status_code == 404
        assert "Not Found." in response.json()["message"]

    @allure.story("Удаление курьера")
    def test_delete_nonexistent_courier(self, courier_api):
        response = courier_api.delete_courier(999999)
        assert response.status_code == 404
        assert "Курьера с таким id нет" in response.json()["message"]

    @allure.story("Удаление курьера")
    def test_delete_courier_twice_fails(self, courier_api, registered_courier):
        # 1. Проверяем, что курьер существует через логин
        login_response = courier_api.login_courier(
            registered_courier["data"]["login"],
            registered_courier["data"]["password"]
        )

        # Если логин не удался, создаем нового курьера
        if login_response.status_code != 200:
            # Создаем нового курьера
            create_response = courier_api.create_courier(**registered_courier["data"])
            if create_response.status_code != 201:
                pytest.fail(f"Не удалось создать курьера: {create_response.text}")

            # Повторно логинимся
            login_response = courier_api.login_courier(
                registered_courier["data"]["login"],
                registered_courier["data"]["password"]
            )
            if login_response.status_code != 200:
                pytest.fail(f"Не удалось войти после создания: {login_response.text}")

        # Получаем актуальный ID курьера
        courier_id = login_response.json().get("id")

        # 2. Первое удаление
        first_response = courier_api.delete_courier(courier_id)
        assert first_response.status_code == 200, \
            f"Первое удаление не удалось: {first_response.text}"

        # 3. Повторное удаление
        second_response = courier_api.delete_courier(courier_id)
        assert second_response.status_code == 404, \
            f"Ожидался код 404, получен {second_response.status_code}"
        assert "Курьера с таким id нет" in second_response.json()["message"], \
            "Неверное сообщение об ошибке"


@allure.epic("API Яндекс.Самокат")
class TestOrderAcceptance:
    @allure.story("Принятие заказа")
    def test_accept_order_success(self, order_api, registered_courier, created_order):
        order_id = order_api.get_order_by_track(created_order).json()["order"]["id"]
        response = order_api.accept_order(order_id, registered_courier["id"])
        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.story("Принятие заказа")
    def test_accept_order_missing_courier_id(self, order_api, created_order):
        order_id = order_api.get_order_by_track(created_order).json()["order"]["id"]
        response = requests.put(f"{TestData.BASE_URL}/api/v1/orders/accept/{order_id}")
        assert response.status_code == 400
        assert "Недостаточно данных" in response.json()["message"]

    @allure.story("Принятие заказа")
    def test_accept_order_invalid_courier_id(self, order_api, created_order):
        order_id = order_api.get_order_by_track(created_order).json()["order"]["id"]
        response = order_api.accept_order(order_id, 999999)
        assert response.status_code == 404
        assert "Курьера с таким id не существует" in response.json()["message"]

    @allure.story("Принятие заказа")
    def test_accept_order_missing_order_id(self, order_api, registered_courier):
        response = requests.put(
            f"{TestData.BASE_URL}/api/v1/orders/accept/?courierId={registered_courier['id']}"
        )
        assert response.status_code == 404
        assert "Not Found." in response.json()["message"]

    @allure.story("Принятие заказа")
    def test_accept_order_invalid_order_id(self, order_api, registered_courier):
        response = order_api.accept_order(999999, registered_courier["id"])
        assert response.status_code == 404
        assert "Заказа с таким id не существует" in response.json()["message"]

    @allure.story("Принятие заказа")
    def test_accept_order_already_accepted(self, order_api, registered_courier, created_order):
        order_id = order_api.get_order_by_track(created_order).json()["order"]["id"]

        # Первое принятие
        first_response = order_api.accept_order(order_id, registered_courier["id"])
        assert first_response.status_code == 200

        # Повторное принятие
        second_response = order_api.accept_order(order_id, registered_courier["id"])
        assert second_response.status_code == 409
        assert "Этот заказ уже в работе" in second_response.json()["message"]


@allure.epic("API Яндекс.Самокат")
class TestOrderRetrieval:
    @allure.story("Получение заказа")
    def test_get_order_by_track_success(self, order_api, created_order):
        response = order_api.get_order_by_track(created_order)
        assert response.status_code == 200
        assert "order" in response.json()

    @allure.story("Получение заказа")
    def test_get_order_missing_track(self):
        response = requests.get(f"{TestData.BASE_URL}/api/v1/orders/track")
        assert response.status_code == 400
        assert "Недостаточно данных" in response.json()["message"]

    @allure.story("Получение заказа")
    def test_get_nonexistent_order(self, order_api):
        response = order_api.get_order_by_track(999999)
        assert response.status_code == 404
        assert "Заказ не найден" in response.json()["message"]

    @allure.story("Получение заказа")
    def test_get_order_with_empty_track(self, order_api):
        response = order_api.get_order_by_track("")
        assert response.status_code == 400
        assert "Недостаточно данных" in response.json()["message"]