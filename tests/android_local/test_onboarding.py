import allure
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

FORWARD_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Forward")
NEXT_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Next")
SKIP_INTERESTS_BUTTON = (AppiumBy.XPATH, "//android.widget.TextView[@text='Skip']")
HOME_TAB = (AppiumBy.ID, "org.wikipedia:id/nav_tab_home")

SCREEN_TITLES = [
    "All the world's knowledge",
    "Data & Privacy",
    "Read in more than 300 languages",
    "Follow your curiosity",
]


def _xpath_text_equals(text: str) -> str:
    if "'" not in text:
        return f"//android.widget.TextView[@text='{text}']"
    return f'//android.widget.TextView[@text="{text}"]'


@allure.title("Прохождение onboarding (4 экрана приветствия) в приложении Wikipedia")
def test_onboarding_screens(driver):
    wait = WebDriverWait(driver, 20)

    for screen_number, expected_title in enumerate(SCREEN_TITLES, start=1):
        with allure.step(f"Экран {screen_number}/4: проверить заголовок '{expected_title}'"):
            title_element = wait.until(
                EC.visibility_of_element_located(
                    (AppiumBy.XPATH, _xpath_text_equals(expected_title))
                )
            )
            allure.attach(
                title_element.text,
                name=f"Экран {screen_number}",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert title_element.text == expected_title

        if screen_number < 4:
            with allure.step(f"Нажать 'Forward' -> экран {screen_number + 1}"):
                wait.until(EC.element_to_be_clickable(FORWARD_BUTTON)).click()
        else:
            with allure.step("На последнем экране нажать 'Next'"):
                wait.until(EC.element_to_be_clickable(NEXT_BUTTON)).click()

    with allure.step("Пропустить экран выбора интересов"):
        wait.until(EC.element_to_be_clickable(SKIP_INTERESTS_BUTTON)).click()

    with allure.step("Проверить, что онбординг завершён - открылся главный экран"):
        home_tab = wait.until(EC.presence_of_element_located(HOME_TAB))
        assert home_tab.is_displayed()