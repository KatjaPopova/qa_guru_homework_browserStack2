import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

CONTEXT = os.getenv("CONTEXT", "local_emulator")

load_dotenv(f".env.{CONTEXT}")

if CONTEXT == "bstack":
    if Path(".env.credentials").exists():
        load_dotenv(".env.credentials")
    else:
        load_dotenv(".env")


class Settings(BaseSettings):
    context: str = CONTEXT

    platform_name: str = "android"
    device_name: str = "emulator-5554"
    platform_version: str = "13.0"
    app: str = ""
    udid: str | None = None

    appium_server_url: str = "http://127.0.0.1:4723"

    browserstack_username: str | None = None
    browserstack_access_key: str | None = None
    browserstack_url: str = "hub.browserstack.com"
    ios_app: str = "bs://sample.app"
    project_name: str = "QA Guru Homework"
    build_name: str = "browserstack-build-1"

    model_config = SettingsConfigDict(extra="ignore")


settings = Settings()

if settings.context == "bstack":
    if not settings.browserstack_username or not settings.browserstack_access_key:
        raise RuntimeError(
            "Для CONTEXT=bstack нужны BROWSERSTACK_USERNAME и "
            "BROWSERSTACK_ACCESS_KEY в файле .env.credentials (или .env)."
        )
