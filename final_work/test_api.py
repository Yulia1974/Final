import pytest
import requests
import allure

BASE_URL = "https://api.kinopoisk.dev/v1.4/movie/search"
SEARCH_ENDPOINT = "/search"


# Фикстура для актуального токена
@pytest.fixture
def valid_token():
    return "B4CQE8A-PF7MM8T-G1NAH9B-7CH3MTH"


# Фикстура для неактуального или просроченного токена
@pytest.fixture
def invalid_token():
    return "invalid_or_expired_token"


# Общая функция для выполнения поиска
def search_movie(query, token=None):
    headers = {}
    if token:
        headers['X-API-Key'] = token
    params = {'query': query}
    response = requests.get(f"{BASE_URL}{SEARCH_ENDPOINT}", headers=headers, params=params)
    return response


@allure.feature("Поиск фильмов")
@allure.story("Поиск по названию фильма на кириллице")
def test_search_by_cyrillic_title(valid_token):
    query = "Брат"
    response = search_movie(query, token=valid_token)
    with ((((allure.step("Проверка успешного ответа и наличия результатов"))))):
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
        data = response.json()
        assert 'results' in data, "В ответе отсутствует 'results'"
        assert any('Брат' in result['title'] for result in data['results']), "Фильм с названием 'Брат' не найден"


@allure.feature("Поиск фильмов")
@allure.story("Поиск по названию фильма на латинице")
def test_search_by_latin_title(valid_token):
    query = "Inception"
    response = search_movie(query, token=valid_token)
    with allure.step("Проверка успешного ответа и наличия результатов"):
        assert response.status_code == 200
        data = response.json()
        assert 'results' in data
        assert any('Inception' in result['title'] for result in data['results'])


@allure.feature("Поиск фильмов")
@allure.story("Поиск по названию фильма с цифрами")
def test_search_with_numbers(valid_token):
    query = "007"
    response = search_movie(query, token=valid_token)
    with allure.step("Проверка успешного ответа и наличия результатов"):
        assert response.status_code == 200
        data = response.json()
        assert 'results' in data


@allure.feature("Поиск фильмов")
@allure.story("Поиск по произвольному набору символов")
def test_search_with_random_symbols(valid_token):
    query = "!@#$%^&*()_+"
    response = search_movie(query, token=valid_token)
    with allure.step("Проверка ответа без ошибок"):
        # Возможно, результат будет пустым или с ошибкой поиска
        if response.status_code == 200:
            data = response.json()
            assert 'results' in data
        else:
            assert response.status_code == 200 or response.status_code == 204


@allure.feature("Поиск фильмов")
@allure.story("Пустой поиск")
def test_empty_search(valid_token):
    query = ""
    response = search_movie(query, token=valid_token)
    with allure.step("Проверка реакции API на пустой запрос"):
        assert response.status_code in [200, 400]
        if response.status_code == 200:
            data = response.json()


@allure.feature("Поиск фильмов")
@allure.story("Поиск без токена")
def test_search_without_token():
    query = "Титаник"
    response = search_movie(query)
    with allure.step("Проверка реакции API при отсутствии токена"):
        assert response.status_code in [200, 401]
        if response.status_code == 401:
            data = response.json()
            assert 'error' in data or 'Unauthorized' in data.get('message', '')
        else:
            data = response.json()
            assert 'results' in data


@allure.feature("Поиск фильмов")
@allure.story("Поиск с неактуальным токеном")
def test_search_with_expired_token(invalid_token):
    query = "Матрица"
    response = search_movie(query, token=invalid_token)
    with allure.step("Проверка реакции API при использовании неактуального токена"):
        # Ожидается ошибка авторизации
        assert response.status_code == 401 or response.status_code == 403
        data = response.json()
        assert 'error' in data or 'Unauthorized' in data.get('message', '')
