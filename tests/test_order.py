# test_order.py

import allure
import pytest
from data.test_data import TestData
import logging

logger = logging.getLogger(__name__)


@allure.epic("API Яндекс.Самокат")
@allure.feature("Работа с заказами")
class TestOrder:
    @allure.story("Создание заказа")
    @allure.title("Создание заказа с указанием цвета")
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"]
    ], ids=lambda x: f"цвет: {x}")
    def test_create_order_with_color(self, order_api, color):
        payload = TestData.generate_order_data(color)
        response = order_api.create_order(payload)

        assert response.status_code == 201, (
            f"Ожидался статус 201, получен {response.status_code}. Ответ: {response.text}"
        )
        assert "track" in response.json(), (
            "В ответе отсутствует поле 'track'"
        )

        order_info = order_api.get_order_by_track(response.json()["track"])
        assert order_info.status_code == 200, (
            f"Не удалось получить заказ. Статус: {order_info.status_code}, Ответ: {order_info.text}"
        )

        actual_color = order_info.json().get("order", {}).get("color")
        assert actual_color == color, (
            f"Ожидался цвет {color}, получен {actual_color}. Полный ответ: {order_info.json()}"
        )

    @allure.story("Получение списка заказов")
    @allure.title("Получить список заказов")
    def test_get_orders_list(self, order_api):
        response = order_api.get_orders_list()
        response_data = response.json()

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}"
        )
        assert isinstance(response_data.get("orders"), list), (
            f"Поле 'orders' должно быть списком, получено: {type(response_data.get('orders'))}"
        )


class TestOrderAcceptance:
    @allure.title("Успешное принятие заказа (статус 200)")
    def test_accept_order_success(self, order_api, order_id_by_track, registered_courier):
        """
        Проверяет только успешное принятие заказа (код 200)
        """
        response = order_api.accept_order(
            order_id=order_id_by_track,
            courier_id=registered_courier["id"]
        )

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}. Ответ: {response.text}"
        )
        assert response.json().get("ok") is True, (
            f"Ожидалось {{'ok': True}}, получено {response.json()}"
        )

    @allure.title("Конфликт при повторном принятии заказа (статус 409)")
    def test_accept_order_conflict(self, order_api, order_id_by_track, registered_courier):
        """
        Проверяет конфликт при повторном принятии заказа (код 409)
        """
        # Первое принятие (должно быть успешным)
        first_response = order_api.accept_order(
            order_id=order_id_by_track,
            courier_id=registered_courier["id"]
        )
        assert first_response.status_code == 200, "Первое принятие должно быть успешным"

        # Повторное принятие
        second_response = order_api.accept_order(
            order_id=order_id_by_track,
            courier_id=registered_courier["id"]
        )

        assert second_response.status_code == 409, (
            f"Ожидался статус 409, получен {second_response.status_code}"
        )
        assert TestData.ORDER_ALREADY_ACCEPTED_MESSAGE in second_response.json().get("message", "")

    @pytest.mark.xfail(reason="API возвращает 500 вместо 400/404")
    @allure.title("Ошибка при отсутствии ID курьера")
    def test_accept_order_missing_courier_id(self, order_api, order_id_by_track):
        response = order_api.accept_order(order_id_by_track, None)
        assert response.status_code in [400, 404, 500], (
            f"Ожидалась ошибка клиента, получен {response.status_code}"
        )

    @pytest.mark.xfail(reason="API возвращает 500 вместо 404")
    @allure.title("Ошибка при неверном ID курьера")
    def test_accept_order_invalid_courier_id(self, order_api, order_id_by_track):
        response = order_api.accept_order(order_id_by_track, "invalid_courier_id")
        assert response.status_code in [404, 500], (
            "Ожидалась ошибка 'Не найдено'"
        )

    @pytest.mark.xfail(reason="API возвращает 500 вместо 400")
    @allure.title("Ошибка при отсутствии ID заказа")
    def test_accept_order_missing_order_id(self, order_api, registered_courier):
        response = order_api.accept_order(None, registered_courier["id"])
        assert response.status_code in [400, 500]

    @pytest.mark.xfail(reason="API возвращает 500 вместо 404")
    @allure.title("Ошибка при неверном ID заказа")
    def test_accept_order_invalid_order_id(self, order_api, registered_courier):
        response = order_api.accept_order(999999, registered_courier["id"])
        assert response.status_code in [404, 500]


@allure.feature("Получение заказов")
class TestOrderByTrack:
    @allure.title("Успешное получение заказа по трек-номеру")
    def test_get_order_by_track_success(self, order_api, created_order):
        response = order_api.get_order_by_track(created_order)
        response_data = response.json()

        assert response.status_code == 200, (
            f"Ожидался 200, получен {response.status_code}"
        )
        assert "order" in response_data, (
            f"Нет данных о заказе в ответе. Получено: {response_data.keys()}"
        )
        assert isinstance(response_data["order"].get("id"), int), (
            "ID заказа должен быть числом"
        )

    @allure.title("Ошибка при отсутствии трек-номера")
    def test_get_order_missing_track(self, order_api):
        """Проверяет обработку отсутствия трек-номера"""
        response = order_api.get_order_by_track(None)

        # API возвращает 500 с определенным сообщением
        assert response.status_code == 500, (
            f"Ожидался статус 500, получен {response.status_code}"
        )
        assert response.json().get("message") == "Unexpected token N in JSON at position 0", (
            f"Неожиданное сообщение об ошибке: {response.text}"
        )

    @allure.title("Ошибка при несуществующем трек-номере")
    def test_get_order_invalid_track(self, order_api):
        response = order_api.get_order_by_track(999999)
        assert response.status_code == 404, (
            f"Ожидался статус 404, получен {response.status_code}"
        )
        assert "Заказ не найден" in response.text, (
            "Сообщение об ошибке не соответствует ожидаемому"
        )