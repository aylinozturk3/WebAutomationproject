from base import  WebDriverController, ConfigManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

class DiscordPage(WebDriverController):
    def __init__(self, driver, config_file):
        super().__init__(driver, config_file)
        self.url = 'https://discord.com/'
        self.ui_controller = WebDriverController(driver, config_file)

    def start_video_call(self, duration: int, email: str, password: str) -> bool:
        result = True
        self.ui_controller.get(self.url)

        if self.ui_controller.wait_until("login", "login_button", timeout=10):
           self.ui_controller.find_element("login", "login_button").click()

        result &=self.login_(email, password)

        if result:
           if self.ui_controller.wait_until("call", "search_bar",timeout=20):
              self.ui_controller.find_element("call","search_bar").click()

           username = input("Enter the username to call: ")
           if self.ui_controller.wait_until("call", "search_bar2",timeout=20):
              self.ui_controller.find_element("call","search_bar2").send_keys(username)
              time.sleep(5)
              self.ui_controller.find_element("call", "search_bar2").send_keys(Keys.RETURN)

           time.sleep(5)
           try:
              self.start_call(duration)
           except NoSuchElementException as e:
              print(f"Error: {e}")
              result = False

        else:
            result=False

        return result

    def login_(self,  email: str,password: str) ->bool:  # Performs the login process using provided email and password

        if self.ui_controller.wait_until("login", "email",timeout=10):
           self.ui_controller.find_element("login","email").send_keys(email)


        if self.ui_controller.wait_until("login", "password", timeout=10):
           self.ui_controller.find_element("login", "password").send_keys(password)

        if self.ui_controller.wait_until("login", "login_button2", timeout=5):
           self.ui_controller.find_element("login", "login_button2").click()

        return self.ui_controller.wait_until("login", "verify_element", timeout=20) is not None

    def start_call(self, duration: int) -> bool:
        time.sleep(5)
        if self.ui_controller.wait_until("call","call_button",timeout=20):
           self.ui_controller.find_element("call","call_button").click()
           time.sleep(duration)

