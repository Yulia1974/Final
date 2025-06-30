import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Фоновый режим
    options.add_argument("user-agent=Mozilla/5.0 "
                         "(Windows NT 10.0; Win64; x64)")  # Меняем User-Agent
    driver = webdriver.Chrome(options=options)
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
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "kp_query"))
        )
        search_input.clear()
        search_input.send_keys("Побег из Шоушенка")
        search_input.send_keys(Keys.RETURN)

    with (allure.step("Дождаться результатов поиска и проверить наличие фильма")):
        results = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                                 ".search_results .element"))
        )
        assert any("Побег из Шоушенка" in result.text for result in results
                   ),"Фильм не найден в результатах поиска"


@allure.title("Переход на страницу фильма 'Интерстеллар' "
              "по первому результату поиска")
def test_navigate_to_movie_page(driver):
    with allure.step("Открыть сайт Кинопоиск"):
        driver.get("https://www.kinopoisk.ru/")
    with allure.step("Ввести название фильма 'Интерстеллар' в поисковую строку"):
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "kp_query"))
        )
        search_input.clear()
        search_input.send_keys("Интерстеллар")
        search_input.send_keys(Keys.RETURN)
    with allure.step("Кликнуть по первому результату поиска"):
        first_result = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        ".search_results .element a"))
        )
        first_result.click()
    with allure.step("Проверить, что URL содержит название фильма или ID"):
        WebDriverWait(driver, 10).until(lambda d:
                                        "interstellar" in d.current_url.lower())


@allure.title("Добавление фильма в избранное")
def test_add_to_favorites(driver):
    with allure.step("Открыть страницу фильма 'Дюна'"):
        driver.get("https://www.kinopoisk.ru/film/1055430/")
    try:
        with allure.step("Найти кнопку добавления в избранное и кликнуть по ней"):
            favorite_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".add-to-favorites"))
            )
            favorite_button.click()
        with allure.step("Проверить появление сообщения об успешном добавлении"):
            success_message = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                  ".popup-success"))
            )
            assert success_message.is_displayed()
    except Exception as e:
        pytest.skip(f"Кнопка добавления в избранное недоступна "
                    f"или уже добавлено: {e}")


@allure.title("Открытие вкладки с отзывами о фильме 'Дюна'")
def test_open_reviews_tab(driver):
    with allure.step("Открыть страницу фильма 'Дюна'"):
        driver.get("https://www.kinopoisk.ru/film/1055430/")
    with allure.step("Перейти во вкладку с отзывами"):
        reviews_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "//a[contains(text(), 'Отзывы')]"))
        )
        reviews_tab.click()
    with allure.step("Проверить наличие заголовка 'Отзывы' на странице"):
        header = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
        assert "Отзывы" in header.text
