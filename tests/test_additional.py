# test_additional.py

import allure
import requests
from data.test_data import TestData


@allure.epic("API Яндекс.Самокат")
class TestCourierDeletion:
    @allure.story("Удаление курьера")
    @allure.title("Удаление курьера по ID из фикстуры")
    def test_delete_by_fixture_id(self, courier_api, registered_courier):
        """Проверяет удаление курьера с использованием ID из фикстуры"""
        response = courier_api.delete_courier(registered_courier["id"])
        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.story("Удаление курьера")
    @allure.title("Ошибка при отсутствии ID курьера")
    def test_delete_courier_missing_id(self):
        response = requests.delete(f"{TestData.BASE_URL}/api/v1/courier/")
        assert response.status_code == 404
        assert TestData.NOT_FOUND_MESSAGE in response.json()["message"]

    @allure.story("Удаление курьера")
    @allure.title("Ошибка при удалении несуществующего курьера")
    def test_delete_nonexistent_courier(self, courier_api):
        response = courier_api.delete_courier(999999)
        assert response.status_code == 404
        assert TestData.COURIER_NOT_FOUND_MESSAGE in response.json()["message"]

    @allure.story("Удаление курьера")
    @allure.title("Удаление курьера с получением ID через логин")
    def test_delete_with_login(self, courier_api, registered_courier):
        """Проверяет полный цикл: логин -> получение ID -> удаление"""
        login_response = courier_api.login_courier(
            registered_courier["data"]["login"],
            registered_courier["data"]["password"]
        )
        assert login_response.status_code == 200, "Курьер должен существовать"

        courier_id = login_response.json()["id"]
        response = courier_api.delete_courier(courier_id)

        assert response.status_code == 200, "Удаление должно быть успешным"
        assert response.json() == {"ok": True}

    @allure.story("Удаление курьера")
    @allure.title("Ошибка при повторном удалении курьера")
    def test_delete_courier_twice_fails(self, courier_api, courier_data):  # Используем courier_data
        # 1. Создаем нового курьера
        create_response = courier_api.create_courier(**courier_data)
        assert create_response.status_code == 201, "Не удалось создать курьера"

        # 2. Получаем ID через логин
        login_response = courier_api.login_courier(
            courier_data["login"],
            courier_data["password"]
        )
        assert login_response.status_code == 200, "Не удалось войти под новым курьером"
        courier_id = login_response.json()["id"]

        # 3. Первое удаление
        first_response = courier_api.delete_courier(courier_id)
        assert first_response.status_code == 200, "Первое удаление должно быть успешным"

        # 4. Повторное удаление
        second_response = courier_api.delete_courier(courier_id)
        assert second_response.status_code == 404, "Ожидалась ошибка 404 при повторном удалении"
        assert TestData.COURIER_NOT_FOUND_MESSAGE in second_response.json().get("message", "")


@allure.epic("API Яндекс.Самокат")
class TestOrderAcceptance:
    @allure.story("Принятие заказа")
    @allure.title("Успешное принятие заказа")
    def test_accept_order_success(self, order_api, registered_courier, order_id_by_track):
        response = order_api.accept_order(order_id_by_track, registered_courier["id"])
        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.story("Принятие заказа")
    @allure.title("Ошибка при отсутствии ID курьера")
    def test_accept_order_missing_courier_id(self, order_api, order_id_by_track):
        response = requests.put(f"{TestData.BASE_URL}/api/v1/orders/accept/{order_id_by_track}")
        assert response.status_code == 400
        assert TestData.INSUFFICIENT_DATA_MESSAGE in response.json()["message"]

    @allure.story("Принятие заказа")
    @allure.title("Ошибка при неверном ID курьера")
    def test_accept_order_invalid_courier_id(self, order_api, order_id_by_track):
        response = order_api.accept_order(order_id_by_track, 999999)
        assert response.status_code == 404
        assert TestData.COURIER_NOT_EXIST_MESSAGE in response.json()["message"]

    @allure.story("Принятие заказа")
    @allure.title("Ошибка при отсутствии ID заказа")
    def test_accept_order_missing_order_id(self, order_api, registered_courier):
        response = requests.put(
            f"{TestData.BASE_URL}/api/v1/orders/accept/?courierId={registered_courier['id']}"
        )
        assert response.status_code == 404
        assert TestData.NOT_FOUND_MESSAGE in response.json()["message"]

    @allure.story("Принятие заказа")
    @allure.title("Ошибка при неверном ID заказа")
    def test_accept_order_invalid_order_id(self, order_api, registered_courier):
        response = order_api.accept_order(999999, registered_courier["id"])
        assert response.status_code == 404
        assert TestData.ORDER_NOT_EXIST_MESSAGE in response.json()["message"]

    @allure.story("Принятие заказа")
    @allure.title("Ошибка при повторном принятии заказа")
    def test_accept_order_already_accepted(self, order_api, registered_courier, order_id_by_track):
        # Первое принятие
        first_response = order_api.accept_order(order_id_by_track, registered_courier["id"])
        assert first_response.status_code == 200

        # Повторное принятие
        second_response = order_api.accept_order(order_id_by_track, registered_courier["id"])
        assert second_response.status_code == 409
        assert TestData.ORDER_ALREADY_ACCEPTED_MESSAGE in second_response.json()["message"]


@allure.epic("API Яндекс.Самокат")
class TestOrderRetrieval:
    @allure.story("Получение заказа")
    @allure.title("Успешное получение заказа по трек-номеру")
    def test_get_order_by_track_success(self, order_api, created_order):
        response = order_api.get_order_by_track(created_order)
        assert response.status_code == 200
        assert "order" in response.json()

    @allure.story("Получение заказа")
    @allure.title("Ошибка при отсутствии трек-номера")
    def test_get_order_missing_track(self):
        response = requests.get(f"{TestData.BASE_URL}/api/v1/orders/track")
        assert response.status_code == 400
        assert TestData.INSUFFICIENT_DATA_MESSAGE in response.json()["message"]

    @allure.story("Получение заказа")
    @allure.title("Ошибка при несуществующем трек-номере")
    def test_get_nonexistent_order(self, order_api):
        response = order_api.get_order_by_track(999999)
        assert response.status_code == 404
        assert TestData.ORDER_NOT_FOUND_MESSAGE in response.json()["message"]

    @allure.story("Получение заказа")
    @allure.title("Ошибка при пустом трек-номере")
    def test_get_order_with_empty_track(self, order_api):
        response = order_api.get_order_by_track("")
        assert response.status_code == 400
        assert TestData.INSUFFICIENT_DATA_MESSAGE in response.json()["message"]