from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from base import WebDriverController, ConfigManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

class MicrosoftTeams(WebDriverController):
    def __init__(self, driver, config_file):
        super().__init__(driver, config_file)
        self.url = 'https://teams.microsoft.com/v2/'
        self.ui_controller = WebDriverController(driver, config_file)

    def text_message(self, text:str, email:str, password:str):
        result = True
        self.login_without_login(self.url)

        result &= self.login_(email, password)

        if result:
              if self.ui_controller.wait_until("login","extra_hesap_secim",timeout=30):
                  self.ui_controller.find_element("login","extra_hesap_secim").click()
              if self.ui_controller.wait_until("text", "pop_up", timeout=40):
                  self.ui_controller.find_element("text", "pop_up").click()
              try:
                  self.texting_(text)
                  time.sleep(20)
              except NoSuchElementException as e:
                  print(f"Error: {e}")
                  result = False
        else:
            result=False

        return result

    def texting_(self, text: str) -> bool:
        result = True

        if self.ui_controller.wait_until("text", "text_area", timeout=40):
            self.ui_controller.find_element("text","text_area").send_keys(text)

        if self.ui_controller.wait_until("text", "send_button", timeout=30):
            self.ui_controller.find_element("text", "send_button").click()

        time.sleep(5)
        return result

    def login_without_login(self, url) -> bool:
        result = True
        self.ui_controller.open_url(url)

        return result

    def login_(self, email: str, password: str) -> bool:
        result=True
        if self.ui_controller.wait_until("login", "email", timeout=20):
           self.ui_controller.find_element("login", "email").send_keys(email)

        if self.ui_controller.wait_until("login", "continue_button", timeout=20):
           self.ui_controller.find_element("login", "continue_button").click()

        time.sleep(5)
        if self.ui_controller.wait_until("login", "password", timeout=20):
           self.ui_controller.find_element("login", "password").send_keys(password)

        if self.ui_controller.wait_until("login", "login_button2", timeout=20):
           self.ui_controller.find_element("login", "login_button2").click()

        if self.ui_controller.wait_until("login","oturumacikkalsin",timeout=20):
           self.ui_controller.find_element("login","oturumacikkalsin").click()


        return result
