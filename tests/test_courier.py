# test_courier.py

import allure
import pytest

@allure.epic("API Яндекс.Самокат")
@allure.feature("Работа с курьерами")
class TestCourier:
    @allure.story("Авторизация")
    @allure.title("Успешный логин")
    def test_login_success(self, courier):
        response = courier["api"].login_courier(
            login=courier["data"]["login"],
            password=courier["data"]["password"]
        )
        assert response.status_code == 200
        assert "id" in response.json()

    @allure.story("Авторизация")
    @allure.title("Неверный пароль")
    def test_login_wrong_password(self, courier):
        response = courier["api"].login_courier(
            login=courier["data"]["login"],
            password="wrong_password"
        )
        assert response.status_code == 404

    @allure.story("Создание")
    @allure.title("Дубликат курьера")
    def test_duplicate_courier(self, courier):
        response = courier["api"].create_courier(**courier["data"])
        assert response.status_code == 409
        assert "Этот логин уже используется" in response.json()["message"]

    @allure.story("Валидация")
    @allure.title("Отсутствует поле {field}")
    @pytest.mark.parametrize("field", ["login", "password", "firstName"])
    def test_missing_field(self, courier, field):
        test_data = courier["data"].copy()
        del test_data[field]
        response = courier["api"].create_courier(**test_data)
        assert response.status_code == 400