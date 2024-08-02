from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from base import WebDriverController, ConfigManager  # Import your base class
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

class SkypePage(WebDriverController):
    def __init__(self, driver, config_file):
        super().__init__(driver, config_file)
        self.url = 'https://www.skype.com/tr/'
        self.ui_controller = WebDriverController(driver, config_file)

    def start_video_call(self, duration:int, email:str, password:str):
        result = True
        self.login_without_login(self.url)

        if self.ui_controller.wait_until("login", "login_button", timeout=10):
            self.ui_controller.find_element("login", "login_button").click()

        result &= self.login_(email, password)
        if self.ui_controller.wait_until("login", "oturumacikkalsin", timeout=10):
            self.ui_controller.find_element("login", "oturumacikkalsin").click()

        if self.ui_controller.wait_until("call","okey_button",timeout=20):
            self.ui_controller.find_element("call","okey_button").click()

        kullanici_adi = str(input("kullanici adi giriniz: "))

        if self.ui_controller.wait_until("call", "search_box",timeout=20):
            self.ui_controller.find_element("call","search_box").click()

        if self.ui_controller.wait_until("call", "search_box2", timeout=20):
            self.ui_controller.find_element("call", "search_box2").send_keys(kullanici_adi)

        time.sleep(5)
        for _ in range(2):
            self.ui_controller.find_element("call", "search_box2").send_keys(Keys.RETURN)

        try:
            result &= self.start_call(duration)
        except NoSuchElementException as e:
            print(f"Error: {e}")
            result = False

        return result

    def login_without_login(self, url) -> bool:
        result = True
        self.open_url(self.url)
        return result

    def login_(self, email: str, password: str) -> bool:
        if self.ui_controller.wait_until("login", "email", timeout=10):
            self.ui_controller.find_element("login", "email").send_keys(email)
        if self.ui_controller.wait_until("login", "continue_button", timeout=10):
            self.ui_controller.find_element("login", "continue_button").click()

        if self.ui_controller.wait_until("login", "password", timeout=10):
            self.ui_controller.find_element("login", "password").send_keys(password)

        if self.ui_controller.wait_until("login", "login_button2", timeout=10):
            self.ui_controller.find_element("login", "login_button2").click()

        return self.ui_controller.wait_until("login", "verify_element", timeout=20) is not None

    def start_call(self, duration:int) -> bool:
        result = True
        if self.ui_controller.wait_until("call", "call_button", timeout=20):
            self.ui_controller.find_element("call", "call_button").click()
            time.sleep(duration)
        return result





