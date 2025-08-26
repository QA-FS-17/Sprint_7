# conftest.py

import uuid
import logging
import pytest
from api.courier_api import CourierApi
from api.order_api import OrderApi
from data.test_data import TestData


# Настройка логирования
@pytest.fixture(scope="session", autouse=True)
def setup_logging():
    """Настройка централизованного логирования для всех тестов"""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Файловый обработчик
    file_handler = logging.FileHandler('api_tests.log', mode='w')
    file_handler.setFormatter(formatter)

    # Консольный обработчик
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Очистка старых обработчиков
    logger.handlers.clear()
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Уменьшаем логирование для внешних библиотек
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)


# API клиенты
@pytest.fixture(scope="class")
def courier_api():
    """Фикстура для работы с API курьеров"""
    return CourierApi()


@pytest.fixture(scope="class")
def order_api():
    """Фикстура для работы с API заказов"""
    return OrderApi()


# Генерация тестовых данных
@pytest.fixture
def courier_data():
    """Генерирует уникальные данные курьера для каждого теста"""
    data = TestData.generate_courier_data()
    data["login"] = f"{data['login']}_{uuid.uuid4().hex[:6]}"  # Гарантируем уникальность
    return data


# Работа с курьерами
@pytest.fixture
def registered_courier(courier_api, courier_data):
    """Фикстура для зарегистрированного курьера с гарантированным удалением"""
    # Регистрация курьера
    create_response = courier_api.create_courier(**courier_data)
    if create_response.status_code == 409:  # Если курьер уже существует
        courier_data["login"] = f"{courier_data['login']}_{uuid.uuid4().hex[:4]}"  # Новый уникальный логин
        create_response = courier_api.create_courier(**courier_data)
    assert create_response.status_code == 201, f"Ошибка создания курьера: {create_response.text}"

    # Получение ID курьера
    login_response = courier_api.login_courier(courier_data["login"], courier_data["password"])
    assert login_response.status_code == 200, "Ошибка авторизации курьера"
    courier_id = login_response.json()["id"]

    yield {
        "api": courier_api,
        "data": courier_data,
        "id": courier_id
    }

    # Удаление курьера в финализаторе
    delete_response = courier_api.delete_courier(courier_id)
    if delete_response.status_code != 200:
        logging.warning(f"Не удалось удалить курьера {courier_id}")


# Работа с заказами
@pytest.fixture
def created_order(order_api):
    """Фикстура для создания заказа с автоматической отменой"""
    payload = TestData.generate_order_data()
    response = order_api.create_order(payload)
    assert response.status_code == 201, "Ошибка создания заказа"
    track = response.json()["track"]

    yield track

    # Отмена заказа в финализаторе
    cancel_response = order_api.cancel_order(track)
    if cancel_response.status_code != 200:
        logging.warning(f"Не удалось отменить заказ {track}. Ответ: {cancel_response.text}")


@pytest.fixture
def order_id_by_track(order_api, created_order):
    """Фикстура для получения ID заказа по трек-номеру"""
    response = order_api.get_order_by_track(created_order)
    assert response.status_code == 200, "Ошибка получения заказа"
    order_id = response.json()["order"]["id"]
    return order_id