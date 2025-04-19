# conftest.py

import uuid
from api.courier_api import CourierApi
from api.order_api import OrderApi
from data.test_data import TestData
import logging
import pytest


@pytest.fixture(scope="session", autouse=True)
def setup_logging():
    """Настройка логирования для всех тестов"""
    logger = logging.getLogger()  # Корневой логгер
    logger.setLevel(logging.INFO)

    # Формат сообщений
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Файловый обработчик
    file_handler = logging.FileHandler('api_tests.log', mode='w')  # 'w' для перезаписи
    file_handler.setFormatter(formatter)

    # Консольный обработчик
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Очистка старых обработчиков и добавление новых
    logger.handlers.clear()
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Включение логирования для requests и urllib3
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    yield  # Важно для корректного закрытия файлов

    # Закрываем обработчики после завершения
    for handler in logger.handlers:
        handler.close()


@pytest.fixture(scope="class")
def courier_api():
    return CourierApi()


@pytest.fixture(scope="class")
def order_api():
    return OrderApi()


@pytest.fixture(scope="function")
def courier_data():
    """Генерирует новые данные курьера для каждого теста"""
    data = TestData.generate_courier_data()
    data["login"] = f"{data['login']}_{uuid.uuid4().hex[:6]}"
    return data


@pytest.fixture(scope="class")
def registered_courier(courier_api):
    data = TestData.generate_courier_data()
    data["login"] = f"{data['login']}_{uuid.uuid4().hex[:6]}"

    # Регистрация курьера
    response = courier_api.create_courier(**data)
    assert response.status_code == 201

    # Получение ID через логин
    login_response = courier_api.login_courier(
        login=data["login"],
        password=data["password"]
    )
    assert login_response.status_code == 200
    courier_id = login_response.json()["id"]

    yield {
        "api": courier_api,
        "data": data,
        "id": courier_id
    }

    # Удаление курьера
    courier_api.delete_courier(courier_id)


@pytest.fixture
def cleanup_couriers(courier_api):
    yield


@pytest.fixture
def created_order(request, order_api):
    payload = TestData.generate_order_data()
    response = order_api.create_order(payload)
    assert response.status_code == 201, "Не удалось создать заказ"
    track = response.json()["track"]

    def cleanup():
        cancel_response = order_api.cancel_order(track)
        # Убираем строгую проверку на 200, так как заказ может быть уже завершен
        if cancel_response.status_code != 200:
            print(f"Warning: Не удалось отменить заказ {track}")

    request.addfinalizer(cleanup)
    return track


@pytest.fixture
def created_courier(courier_api, courier_data):
    """Фикстура для создания и удаления тестового курьера"""
    # Регистрация курьера
    response = courier_api.create_courier(**courier_data)
    assert response.status_code == 201

    yield courier_data  # Возвращаем данные курьера

    # Удаление курьера
    login_response = courier_api.login_courier(
        login=courier_data["login"],
        password=courier_data["password"]
    )
    if login_response.status_code == 200:
        courier_id = login_response.json()["id"]
        courier_api.delete_courier(courier_id)
