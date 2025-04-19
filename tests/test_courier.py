# test_courier.py

import allure
import pytest
import uuid

@allure.epic("API Яндекс.Самокат")
@allure.feature("Работа с курьерами")
class TestCourierCreation:
    @allure.story("Создание курьера")
    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self, courier_api, courier_data):
        response = courier_api.create_courier(**courier_data)
        assert response.status_code == 201
        assert response.json() == {"ok": True}

    @allure.story("Создание курьера")
    @allure.title("Дубликат курьера")
    def test_duplicate_courier(self, courier_api, registered_courier):
        response = courier_api.create_courier(**registered_courier["data"])
        assert response.status_code == 409
        assert "Этот логин уже используется" in response.json()["message"]

    @allure.story("Валидация полей")
    @allure.title("Проверка создания курьера без поля {field}")
    @pytest.mark.parametrize("field,expected_status,expected_message", [
        ("login", 400, "Недостаточно данных для создания учетной записи"),
        ("password", 400, "Недостаточно данных для создания учетной записи"),
        ("firstName", 201, None)
    ])
    def test_missing_field(self, courier_api, courier_data, field, expected_status, expected_message):
        test_data = courier_data.copy()
        test_data[field] = None

        response = courier_api.create_courier(**test_data)
        assert response.status_code == expected_status

        if expected_message:
            assert expected_message in response.json().get("message", "")

@allure.epic("API Яндекс.Самокат")
@allure.feature("Работа с курьерами")
class TestCourierLogin:
    @allure.story("Авторизация")
    @allure.title("Успешный логин")
    def test_login_success(self, registered_courier):
        response = registered_courier["api"].login_courier(
            login=registered_courier["data"]["login"],
            password=registered_courier["data"]["password"]
        )
        assert response.status_code == 200
        assert isinstance(response.json().get("id"), int)

    @allure.story("Авторизация")
    @allure.title("Неверный пароль")
    def test_login_wrong_password(self, registered_courier):
        response = registered_courier["api"].login_courier(
            login=registered_courier["data"]["login"],
            password="wrong_password"
        )
        assert response.status_code == 404

    @allure.story("Авторизация")
    @allure.title("Несуществующий пользователь")
    def test_login_nonexistent_user(self, courier_api):
        response = courier_api.login_courier(
            login="nonexistent_" + str(uuid.uuid4()),
            password="123456"
        )
        assert response.status_code == 404

    @allure.story("Авторизация")
    @allure.title("Отсутствие обязательного поля {field}")
    @pytest.mark.parametrize("field", ["login", "password"])
    def test_login_missing_field(self, courier_api, registered_courier, field):
        data = {"login": registered_courier["data"]["login"], "password": registered_courier["data"]["password"],
                field: ""}

        response = courier_api.login_courier(
            login=data.get("login"),
            password=data.get("password")
        )
        assert response.status_code == 400
