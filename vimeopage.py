from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from base import WebDriverController, ConfigManager
import time
import json

class VimeoPage(WebDriverController):
    def __init__(self, driver, config_file):
        super().__init__(driver, config_file)
        self.url = 'https://vimeo.com/'
        self.ui_controller = WebDriverController(driver, config_file)

    def play_first_video(self, duration: int, email: str, password: str) -> bool:
        result = True
        self.login_without_login(self.url)

        if self.ui_controller.wait_until("login", "login_button", timeout=10):
            self.ui_controller.find_element("login", "login_button").click()
        else:
            print("login button is not found")
            return False

        time.sleep(5)
        result &= self.login_(email, password)

        if result:
           if self.ui_controller.wait_until("video", "watch_button", timeout=10):
               self.ui_controller.find_element("video", "watch_button").click()

           try:
               result &= self.play_video(duration)
           except NoSuchElementException as e:
               print(f"Error: {e}")
               result = False
        else:
            result=False

        return result

    def login_without_login(self, url) -> bool:
        result = True
        self.ui_controller.open_url(url)
        return result

    def login_(self, email: str, password: str) -> bool:
        result = True  # Start with True, assuming success

        if self.ui_controller.wait_until("login", "login_button", timeout=20):
            login_button = self.ui_controller.find_element("login", "login_button")
            self.ui_controller.execute_script("arguments[0].scrollIntoView();", login_button)
            self.ui_controller.execute_script("arguments[0].click();", login_button)
        else:
            print("Login button not found.")
            result = False

        if self.ui_controller.wait_until("login", "email", timeout=20):
            email_field = self.ui_controller.find_element("login", "email")
            self.ui_controller.execute_script("arguments[0].scrollIntoView();", email_field)
            self.ui_controller.execute_script("arguments[0].style.display = 'block';", email_field)
            self.ui_controller.execute_script("arguments[0].focus();", email_field)
            email_field.click()
            email_field.send_keys(email)
        else:
            print("Email field not found.")
            result = False

        if self.ui_controller.wait_until("login", "password", timeout=20):
            password_field = self.ui_controller.find_element("login", "password")
            self.ui_controller.execute_script("arguments[0].scrollIntoView();", password_field)
            self.ui_controller.execute_script("arguments[0].style.display = 'block';", password_field)
            self.ui_controller.execute_script("arguments[0].focus();", password_field)
            password_field.send_keys(password)
        else:
            print("Password field not found.")
            result = False

        if self.ui_controller.wait_until("login", "login_button2", timeout=10):
            login_button2 = self.ui_controller.find_element("login", "login_button2")
            self.ui_controller.execute_script("arguments[0].scrollIntoView();", login_button2)
            self.ui_controller.execute_script("arguments[0].click();", login_button2)
            time.sleep(20)
        else:
            print("Second login button not found.")
            result = False

        return result

    def play_video(self, duration: int) -> bool:
        result = True

        if self.ui_controller.wait_until("video", "video_locator", timeout=20):
            if self.ui_controller.wait_until("video", "play_button", timeout=20):
                self.ui_controller.find_element("video", "play_button").click()

                start_time = time.time()
                while True:
                    current_time = time.time()
                    elapsed_time = current_time - start_time
                    if elapsed_time >= duration:
                        break
                self.ui_controller.close()
            else:
                print("Play button not found.")
                result = False
        else:
            print("Video element not found.")
            result = False

        return result



