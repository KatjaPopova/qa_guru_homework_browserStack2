import allure
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions

from config import settings


def pytest_addoption(parser):
    parser.addoption(
        "--platform",
        action="store",
        default="android",
        choices=["android", "ios"],
        help="Платформа для BrowserStack (используется только при CONTEXT=bstack)",
    )


def _bstack_options(platform):
    if platform == "android":
        options = UiAutomator2Options()
        options.set_capability("app", settings.app)
        options.set_capability("platformName", "android")
        options.set_capability("deviceName", settings.device_name)
        options.set_capability("platformVersion", settings.platform_version)
    else:
        options = XCUITestOptions()
        options.set_capability("app", settings.ios_app)
        options.set_capability("platformName", "iOS")
        options.set_capability("deviceName", "iPhone 14 Pro Max")
        options.set_capability("platformVersion", "16.0")

    options.set_capability("browserstack.user", settings.browserstack_username)
    options.set_capability("browserstack.key", settings.browserstack_access_key)
    options.set_capability("project", settings.project_name)
    options.set_capability("build", settings.build_name)

    remote_url = (
        f"https://{settings.browserstack_username}:"
        f"{settings.browserstack_access_key}@{settings.browserstack_url}/wd/hub"
    )
    return options, remote_url


def _local_options():
    options = UiAutomator2Options()
    options.set_capability("platformName", "android")
    options.set_capability("appium:deviceName", settings.device_name)
    options.set_capability("appium:platformVersion", settings.platform_version)
    options.set_capability("appium:automationName", "UiAutomator2")
    options.set_capability("appium:app", settings.app)
    options.set_capability("appium:autoGrantPermissions", True)
    options.set_capability("appium:newCommandTimeout", 120)
    options.set_capability("appium:fullReset", True)  # <- каждый раз чистим данные, чтобы видеть онбординг
    if settings.udid:
        options.set_capability("appium:udid", settings.udid)

    options.set_capability("appium:appPackage", "org.wikipedia")
    options.set_capability("appium:appActivity", "org.wikipedia.main.MainActivity")

    return options, settings.appium_server_url


@pytest.fixture
def driver(request):
    if settings.context == "bstack":
        platform = request.config.getoption("--platform")
        options, remote_url = _bstack_options(platform)
        options.set_capability("name", request.node.name)
    else:
        options, remote_url = _local_options()

    drv = webdriver.Remote(remote_url, options=options)

    if settings.context == "bstack":
        session_id = drv.session_id
        dashboard_link = f"https://app-automate.browserstack.com/dashboard/v2/sessions/{session_id}"
        allure.dynamic.link(dashboard_link, name="BrowserStack session (видео, логи)")

    yield drv
    drv.quit()