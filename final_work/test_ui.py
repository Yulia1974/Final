import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import UI_URL, DUNE_URL, OHO_URL


@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 "
                         "(Windows NT 10.0; Win64; x64)")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get(UI_URL)
    yield driver
    driver.quit()


@allure.title("Проверка, что заголовок содержит 'Кинопоиск'")
def test_title_contains_kinopoisk(driver):
    with allure.step("Дождаться полной загрузки сайта Кинопоиск"):
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-tid="911e2f4d"]'))
        )
    with allure.step("Проверить, что заголовок содержит 'Кинопоиск'"):
        assert "Кинопоиск" in driver.title


@allure.title("Поиск фильма 'Побег из Шоушенка' и проверка результатов")
def test_search_movie(driver):
    with allure.step("Дождаться полной загрузки сайта Кинопоиск"):
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-tid="911e2f4d"]'))
        )
    with allure.step("Ввести название фильма в поисковую строку"):
        search_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "kp_query"))
        )
        search_input.clear()
        search_input.send_keys("Побег из Шоушенка")
        search_input.send_keys(Keys.RETURN)

    with (allure.step("Дождаться результатов поиска и проверить наличие фильма")):
        results = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                                 '[data-tid="75209b22"]'))
        )
        assert any("Побег из Шоушенка" in result.text for result in results
                   ), "Фильм не найден в результатах поиска"


@allure.title("Переход на страницу фильма 'Интерстеллар' "
              "по первому результату поиска")
def test_navigate_to_movie_page(driver):
    with allure.step("Дождаться полной загрузки сайта Кинопоиск"):
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-tid="911e2f4d"]'))
        )
    with allure.step("Ввести название фильма 'Интерстеллар' в поисковую строку"):
        search_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "kp_query"))
        )
        search_input.clear()
        search_input.send_keys("Интерстеллар")
        search_input.send_keys(Keys.RETURN)
    with allure.step("Кликнуть по первому результату поиска"):
        first_result = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "//a[text()='Интерстеллар']"))
        )
        first_result.click()
    with allure.step("Проверить, что URL содержит ID фильма"):
        WebDriverWait(driver, 10).until(lambda d:
                                        "258687" in d.current_url.lower())


@allure.title("Открытие вкладки с наградами фильма 'Дюна'")
def test_open_awards_tab(driver):
    with allure.step("Дождаться полной загрузки сайта Кинопоиск"):
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-tid="911e2f4d"]'))
        )

    with allure.step("Перейти на страницу фильма 'Дюна'"):
        driver.get(DUNE_URL)

    with allure.step("Перейти во вкладку с наградами"):
        awards_tab = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href*="/awards"]')))
        awards_tab.click()

    with allure.step("Проверить наличие заголовка 'Награды' на странице"):
        header = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'h1 > a[href="/awards/"]'))
        )
        assert "Награды" in header.text


@allure.title("Открытие вкладки с рецензиями фильма 'ОНО'")
def test_open_reviews_page(driver):
    with allure.step("Дождаться полной загрузки сайта Кинопоиск"):
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-tid="911e2f4d"]'))
        )

    with allure.step("Перейти на страницу фильма 'ОНО'"):
        driver.get(OHO_URL)

    with allure.step("Перейти во вкладку с рецензиями"):
        awards_tab = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href*="/reviews"]')))
        awards_tab.click()

    with allure.step("Проверить наличие кнопки 'Добавить рецензию' на странице"):
        button = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((
                By.CSS_SELECTOR, "a.formReviewAncor:nth-of-type(2)"))
        )
        assert "Добавить рецензию" in button.text
