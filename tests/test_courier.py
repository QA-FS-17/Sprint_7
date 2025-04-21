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

        # Проверка статуса и тела ответа
        assert response.status_code == 201
        assert response.json() == {"ok": True}, (
            f"Ожидалось {{'ok': True}}, получено {response.json()}"
        )

    @allure.story("Создание курьера")
    @allure.title("Дубликат курьера")
    def test_duplicate_courier(self, courier_api, registered_courier):
        response = courier_api.create_courier(**registered_courier["data"])

        # Проверка статуса и сообщения об ошибке
        assert response.status_code == 409
        error_message = response.json().get("message", "")
        assert "Этот логин уже используется" in error_message, (
            f"Ожидалось сообщение 'Этот логин уже используется', получено '{error_message}'"
        )

    @allure.story("Валидация полей")
    @allure.title("Проверка создания курьера без поля {field}")
    @pytest.mark.parametrize("field,expected_status,expected_message", [
        ("login", 400, "Недостаточно данных для создания учетной записи"),
        ("password", 400, "Недостаточно данных для создания учетной записи"),
        ("firstName", 201, "")
    ])
    def test_missing_field(self, courier_api, courier_data, field, expected_status, expected_message):
        test_data = courier_data.copy()
        test_data[field] = None

        response = courier_api.create_courier(**test_data)

        # Проверка статуса
        assert response.status_code == expected_status, (
            f"Ожидался статус {expected_status}, получен {response.status_code}"
        )

        # Проверка сообщения (унифицировано для всех случаев)
        response_message = response.json().get("message", "")
        assert expected_message in response_message, (
            f"Ожидалось сообщение '{expected_message}', получено '{response_message}'"
        )


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

        # Проверка статуса, типа ID и наличия поля 'id'
        assert response.status_code == 200
        response_data = response.json()
        assert "id" in response_data, "В ответе отсутствует поле 'id'"
        assert isinstance(response_data["id"], int), (
            f"ID курьера должен быть int, получен {type(response_data['id'])}"
        )

    @allure.story("Авторизация")
    @allure.title("Неверный пароль")
    def test_login_wrong_password(self, registered_courier):
        response = registered_courier["api"].login_courier(
            login=registered_courier["data"]["login"],
            password="wrong_password"
        )

        # Проверка статуса и сообщения об ошибке
        assert response.status_code == 404
        error_message = response.json().get("message", "")
        assert "Учетная запись не найдена" in error_message, (
            f"Ожидалось сообщение 'Учетная запись не найдена', получено '{error_message}'"
        )

    @allure.story("Авторизация")
    @allure.title("Несуществующий пользователь")
    def test_login_nonexistent_user(self, courier_api):
        fake_login = "nonexistent_" + str(uuid.uuid4())
        response = courier_api.login_courier(
            login=fake_login,
            password="123456"
        )

        # Проверка статуса и сообщения
        assert response.status_code == 404
        error_message = response.json().get("message", "")
        assert "Учетная запись не найдена" in error_message, (
            f"Ожидалось сообщение 'Учетная запись не найдена', получено '{error_message}'"
        )

    @allure.story("Авторизация")
    @allure.title("Отсутствие обязательного поля {field}")
    @pytest.mark.parametrize("field", ["login", "password"])
    def test_login_missing_field(self, courier_api, registered_courier, field):
        data = {
            "login": registered_courier["data"]["login"],
            "password": registered_courier["data"]["password"]
        }
        data[field] = ""  # Пустое значение вместо отсутствия поля

        response = courier_api.login_courier(**data)

        # Проверка статуса и сообщения
        assert response.status_code == 400
        error_message = response.json().get("message", "")
        assert "Недостаточно данных для входа" in error_message, (
            f"Ожидалось сообщение 'Недостаточно данных для входа', получено '{error_message}'"
        )