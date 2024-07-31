from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from base import  WebDriverController, ConfigManager
import time
import json

class AmazonVideoPage(WebDriverController):
    def __init__(self, driver, config_file):
        super().__init__(driver, config_file)
        self.url = 'https://www.primevideo.com'
        self.ui_controller = WebDriverController(driver, config_file)

    def play_first_video(self, duration: int, email: str, password: str) -> bool:
        result = True
        self.login_without_login(self.url)

        if self.ui_controller.wait_until("login", "login_button", timeout=10):
            self.ui_controller.find_element("login", "login_button").click()
        else:
            print("login button is not found")
            return False

        result &= self.login_(email, password)
        time.sleep(3)

        try:
            result &= self.play_video(duration)
        except NoSuchElementException as e:
            print(f"Error: {e}")
            result = False

        return result

    def play_video(self, duration: int) -> bool:
        result=True

        if self.ui_controller.wait_until("video", "video_element", timeout=10):
            self.ui_controller.find_element("video", "video_element").click()

        if self.ui_controller.wait_until("video", "play_button_locator", timeout=10):
            self.ui_controller.find_element("video", "play_button_locator").click()

            start_time=time.time()
            while True:
                current_time=time.time()
                elapsed_time =current_time-start_time
                if elapsed_time>=duration:
                    break
            self.ui_controller.close()
        else:
            print("Video element or play button not found.")
            result = False

        return result

    def login_without_login(self, url) -> bool:
        result = False
        self.ui_controller.open_url(url)
        if self.ui_controller.wait_until("login", "accept_cookies", timeout=10):
            self.ui_controller.find_element("login", "accept_cookies").click()
            result = True
        return result

    def login_(self,  email: str, password: str) -> bool:
        self.ui_controller.find_element("login", "email").send_keys(email)

        if self.ui_controller.wait_until("login", "continue_button", timeout=10):
            self.ui_controller.find_element("login", "continue_button").click()

        if self.ui_controller.wait_until("login", "password", timeout=10):
            self.ui_controller.find_element("login", "password").send_keys(password)

        if self.ui_controller.wait_until("login", "login_button2", timeout=5):
            self.ui_controller.find_element("login", "login_button2").click()

        return self.ui_controller.wait_until("login", "verify_element", timeout=20) is not None





