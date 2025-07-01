import pytest
import requests
import allure
from config import BASE_API_URL, SEARCH_ENDPOINT, MY_API_TOKEN, INVALID_TOKEN


# Фикстура для актуального токена
@pytest.fixture
def valid_token():
    return MY_API_TOKEN


# Фикстура для неактуального или просроченного токена
@pytest.fixture
def invalid_token():
    return INVALID_TOKEN


# Общая функция для выполнения поиска
def search_movie(query, token=None):
    headers = {}
    if token:
        headers['X-API-Key'] = token
    params = {'query': query}
    response = requests.get(f"{BASE_API_URL}{SEARCH_ENDPOINT}",
                            headers=headers, params=params)
    return response


@allure.feature("Поиск фильмов")
@allure.story("Поиск по названию фильма на кириллице")
def test_search_by_cyrillic_title(valid_token):
    query = "Брат"
    response = search_movie(query, token=valid_token)
    with allure.step("Проверка успешного ответа и "
                         "наличия результатов"):
        assert response.status_code == 200, (f"Unexpected status code:"
                                             f" {response.status_code}")
        try:
            data = response.json()
        except ValueError:
            allure.attach(response.text, name="Invalid response",
                      attachment_type=allure.attachment_type.TEXT)
            pytest.fail("API вернул некорректный JSON. Возможно, "
                    "требуется обновить токен или URL.")


@allure.feature("Поиск фильмов")
@allure.story("Поиск по названию фильма на латинице")
def test_search_by_latin_title(valid_token):
    query = "Inception"
    response = search_movie(query, token=valid_token)
    with allure.step("Проверка успешного ответа и наличия результатов"):
        assert response.status_code == 200
        try:
            data = response.json()
        except ValueError:
            allure.attach(response.text, name="Invalid response",
                      attachment_type=allure.attachment_type.TEXT)
            pytest.fail("API вернул некорректный JSON. Возможно, "
                    "требуется обновить токен или URL.")


@allure.feature("Поиск фильмов")
@allure.story("Поиск по названию фильма с цифрами")
def test_search_with_numbers(valid_token):
    query = "007"
    response = search_movie(query, token=valid_token)
    with allure.step("Проверка успешного ответа и наличия результатов"):
        assert response.status_code == 200
        try:
            data = response.json()
        except ValueError:
            allure.attach(response.text, name="Invalid response",
                      attachment_type=allure.attachment_type.TEXT)
            pytest.fail("API вернул некорректный JSON. Возможно, "
                    "требуется обновить токен или URL.")


@allure.feature("Поиск фильмов")
@allure.story("Поиск по произвольному набору символов")
def test_search_with_random_symbols(valid_token):
    query = "!@#$%^&*()_+"
    response = search_movie(query, token=valid_token)
    with (allure.step("Проверка ответа без ошибок")):
        assert response.status_code == 200 or response.status_code == 400,f"Unexpected status code: {response.status_code}"
        try:
            data = response.json()
        except ValueError:
            allure.attach(response.text, name="Invalid response",
                          attachment_type=allure.attachment_type.TEXT)
            pytest.fail("API вернул некорректный JSON. Возможно, "
                        "требуется обновить токен или URL.")


@allure.feature("Поиск фильмов")
@allure.story("Пустой поиск")
def test_empty_search(valid_token):
    query = ""
    response = search_movie(query, token=valid_token)
    with allure.step("Проверка реакции API на пустой запрос"):
        assert response.status_code in [200, 400]
        try:
            data = response.json()
        except ValueError:
            allure.attach(response.text, name="Invalid response",
                          attachment_type=allure.attachment_type.TEXT)
            pytest.fail("API вернул некорректный JSON. Возможно, "
                        "требуется обновить токен или URL.")


@allure.feature("Поиск фильмов")
@allure.story("Поиск без токена")
def test_search_without_token():
    query = "Титаник"
    response = search_movie(query)
    with allure.step("Проверка реакции API при отсутствии токена"):
        assert response.status_code in [200, 401]
        try:
            data = response.json()
        except ValueError:
            allure.attach(response.text, name="Invalid response",
                          attachment_type=allure.attachment_type.TEXT)
            pytest.fail("API вернул некорректный JSON. Возможно, "
                        "требуется обновить токен или URL.")


@allure.feature("Поиск фильмов")
@allure.story("Поиск с неактуальным токеном")
def test_search_with_expired_token(invalid_token):
    query = "Матрица"
    response = search_movie(query, token=invalid_token)
    with allure.step("Проверка реакции API при использовании "
                     "неактуального токена"):
        # Ожидается ошибка авторизации
        assert response.status_code == 401 or response.status_code == 403
        try:
            data = response.json()
        except ValueError:
            allure.attach(response.text, name="Invalid response",
                          attachment_type=allure.attachment_type.TEXT)
            pytest.fail("API вернул некорректный JSON. Возможно, "
                        "требуется обновить токен или URL.")
