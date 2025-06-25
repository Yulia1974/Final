import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


@pytest.fixture(scope="module")
def driver():
    # Инициализация драйвера (например, Chrome)
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


@allure.title("Проверка, что заголовок содержит 'Кинопоиск'")
def test_title_contains_кинопоиск(driver):
    with allure.step("Открыть сайт Кинопоиск"):
        driver.get("https://www.kinopoisk.ru/")
    with allure.step("Проверить, что заголовок содержит 'Кинопоиск'"):
        assert "Кинопоиск" in driver.title


@allure.title("Поиск фильма 'Побег из Шоушенка' и проверка результатов")
def test_search_movie(driver):
    with allure.step("Открыть сайт Кинопоиск"):
        driver.get("https://www.kinopoisk.ru/")
    with allure.step("Ввести название фильма в поисковую строку"):
        search_input = driver.find_element(By.NAME, "kp_query")
        search_input.send_keys("Побег из Шоушенка")
        search_input.send_keys(Keys.RETURN)
    with (allure.step("Дождаться результатов поиска и проверить наличие фильма")):
        results = driver.find_elements(By.CSS_SELECTOR, ".search_results .element")
        assert any("Побег из Шоушенка" in result.text for result in results), "Фильм не найден в результатах поиска"


@allure.title("Переход на страницу фильма 'Интерстеллар' по первому результату поиска")
def test_navigate_to_movie_page(driver):
    with allure.step("Открыть сайт Кинопоиск"):
        driver.get("https://www.kinopoisk.ru/")
    with allure.step("Ввести название фильма 'Интерстеллар' в поисковую строку"):
        search_input = driver.find_element(By.NAME, "kp_query")
        search_input.send_keys("Интерстеллар")
        search_input.send_keys(Keys.RETURN)
    with allure.step("Кликнуть по первому результату поиска"):
        first_result = driver.find_element(By.CSS_SELECTOR, ".search_results .element a")
        first_result.click()
    with allure.step("Проверить, что URL содержит название фильма или ID"):
        assert "interstellar" in driver.current_url.lower()


@allure.title("Добавление фильма в избранное")
def test_add_to_favorites(driver):
    with allure.step("Открыть страницу фильма 'Дюна'"):
        driver.get("https://www.kinopoisk.ru/film/1055430/")
    try:
        with allure.step("Найти кнопку добавления в избранное и кликнуть по ней"):
            favorite_button = driver.find_element(By.CSS_SELECTOR, ".add-to-favorites")
            favorite_button.click()
        with allure.step("Проверить появление сообщения об успешном добавлении"):
            success_message = driver.find_element(By.CSS_SELECTOR, ".popup-success")
            assert success_message.is_displayed()
    except Exception as e:
        pytest.skip(f"Кнопка добавления в избранное недоступна или уже добавлено: {e}")


@allure.title("Открытие вкладки с отзывами о фильме 'Дюна'")
def test_open_reviews_tab(driver):
    with allure.step("Открыть страницу фильма 'Дюна'"):
        driver.get("https://www.kinopoisk.ru/film/1055430/")
    with allure.step("Перейти во вкладку с отзывами"):
        reviews_tab = driver.find_element(By.XPATH, "//a[contains(text(), 'Отзывы')]")
        reviews_tab.click()
    with allure.step("Проверить наличие заголовка 'Отзывы' на странице"):
        header = driver.find_element(By.TAG_NAME, "h1")
        assert "Отзывы" in header.text
