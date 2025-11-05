import httpx
from django.conf import settings

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def make_wedriver() -> WebDriver:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    if settings.USE_REMOTE_DRIVER:
        return webdriver.Remote(
                command_executor="http://selenium:4444",
                options=chrome_options,
                desired_capabilities=DesiredCapabilities.CHROME
            )
    return webdriver.Chrome(chrome_options=chrome_options)


def make_request_client() -> httpx.Client:
    timeout = httpx.Timeout(15.0, connect=5.0)
    limits = httpx.Limits(max_keepalive_connections=5, max_connections=10)
    client = httpx.Client(timeout=timeout, limits=limits)
    return client

