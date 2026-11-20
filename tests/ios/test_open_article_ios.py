import allure
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

WEB_VIEW_TAB = (AppiumBy.ACCESSIBILITY_ID, "Web View")
ARTICLE_WEBVIEW = (AppiumBy.CLASS_NAME, "XCUIElementTypeWebView")


@allure.title("Открытие WebView-вкладки (iOS sample app)")
def test_open_article(driver):
    wait = WebDriverWait(driver, 30)

    with allure.step("Зафиксировать исходный page_source"):
        page_before_click = driver.page_source

    with allure.step("Кликнуть на вкладку 'Web View'"):
        web_view_tab = wait.until(EC.element_to_be_clickable(WEB_VIEW_TAB))
        web_view_tab.click()

    with allure.step("Дождаться появления WebView-элемента"):
        wait.until(EC.presence_of_element_located(ARTICLE_WEBVIEW))

    with allure.step("Проверить, что экран изменился"):
        assert driver.page_source != page_before_click