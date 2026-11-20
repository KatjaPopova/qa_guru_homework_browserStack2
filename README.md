## Запуск тестов

# Эмулятор
CONTEXT=local_emulator python -m pytest tests/android_local/test_onboarding.py -v

# Реальное устройство
CONTEXT=local_real python -m pytest tests/android_local/test_onboarding.py -v

# BrowserStack
CONTEXT=bstack python -m pytest tests/android --platform android -v
