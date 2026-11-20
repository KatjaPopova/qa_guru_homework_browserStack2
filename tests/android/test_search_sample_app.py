import allure
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@allure.title("Поиск статьи в Wikipedia sample app")
def test_successful_search(driver):
    wait = WebDriverWait(driver, 30)

    with allure.step("Открыть поиск"):
        search_element = wait.until(
            EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia"))
        )
        search_element.click()

    with allure.step("Ввести запрос 'Appium'"):
        insert_text_element = wait.until(
            EC.element_to_be_clickable(
                (AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text")
            )
        )
        insert_text_element.send_keys("Appium")

    with allure.step("Проверить, что результаты поиска не пустые"):
        results = wait.until(
            lambda d: d.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
        )
        allure.attach(str(len(results)), name="Количество найденных элементов", attachment_type=allure.attachment_type.TEXT)
        assert len(results) > 0