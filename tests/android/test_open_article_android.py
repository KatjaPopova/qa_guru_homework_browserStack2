import allure
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@allure.title("Открытие статьи через поиск (Android)")
def test_open_article(driver):
    wait = WebDriverWait(driver, 30)

    with allure.step("Открыть поиск по Википедии"):
        search_icon = wait.until(
            EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia"))
        )
        search_icon.click()

    with allure.step("Ввести поисковый запрос 'Appium'"):
        search_input = wait.until(
            EC.element_to_be_clickable(
                (AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text")
            )
        )
        search_input.send_keys("Appium")

    with allure.step("Дождаться результатов поиска и найти первую статью"):
        first_result = wait.until(
            EC.element_to_be_clickable(
                (AppiumBy.ID, "org.wikipedia.alpha:id/page_list_item_title")
            )
        )
        article_title = first_result.text
        allure.attach(article_title, name="Найденный заголовок статьи", attachment_type=allure.attachment_type.TEXT)
        assert article_title, "Не нашли заголовок статьи в результатах поиска"

    with allure.step("Кликнуть на найденную статью"):
        first_result.click()