from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from base import  WebDriverController, ConfigManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import json

class YahooVideo(WebDriverController):
    def __init__(self, driver, config_file):
        super().__init__(driver, config_file)
        self.url = 'https://www.yahoo.com/entertainment/'
        self.ui_controller = WebDriverController(driver, config_file)

    def play_first_video(self, duration: int, email: str, password: str) -> bool:
        result=True
        self.login_without_login(self.url)

        if self.ui_controller.wait_until("login", "login_button", timeout=10):
            self.ui_controller.find_element("login", "login_button").click()
        else:
            print("login button is not found")
            return False
        result &=self.login_(email,password)

        if result:
           if self.ui_controller.wait_until("video", "more_button",timeout=10):
              self.ui_controller.move_to_element("video", "more_button")


           if self.ui_controller.wait_until("video","videos_button",timeout=10):
              self.ui_controller.find_element("video","videos_button").click()

           if self.ui_controller.wait_until("video","select_video",timeout=10):
               self.ui_controller.find_element("video","select_video").click()
           time.sleep(5)
           try:
               result &= self.play_video(duration)
           except NoSuchElementException as e:
               print(f"Error: {e}")
               result = False

        else:
            result=False

        return result

    def login_without_login(self,url)->bool:#Navigates to the login page without performing login
        result=True
        self.ui_controller.open_url(url)
        return result

    def login_(self, email:str, password:str)->bool:
        self.ui_controller.find_element("login", "email").send_keys(email)
        if self.ui_controller.wait_until("login","continue_button",timeout=10):
            self.ui_controller.find_element("login","continue_button").click()
        if self.ui_controller.wait_until("login","password",timeout=10):
            self.ui_controller.find_element("login","password").send_keys(password)
        if self.ui_controller.wait_until("login","login_button2",timeout=10):
            self.ui_controller.find_element("login","login_button2").click()

        return self.ui_controller.wait_until("login", "verify_element", timeout=20) is not None



    def play_video(self, duration: int) -> bool:
        result = True
        video_elements = self.ui_controller.find_elements("video", "video_element")

        if video_elements:
            actions = ActionChains(self.driver)
            actions.move_to_element(video_elements[0]).perform()
            time.sleep(duration)
            video_elements[0].click()
            time.sleep(2)

        return result


