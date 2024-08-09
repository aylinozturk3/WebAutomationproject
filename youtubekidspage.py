from base import WebDriverController, ConfigManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
import datetime
import logging

class YoutubeKidsPage(WebDriverController):
    def __init__(self, driver, config_file):
        super().__init__(driver, config_file)
        self.url = 'https://www.youtubekids.com'
        self.ui_controller = WebDriverController(driver, config_file)

    def select_account(self):
        try:
            account_num = int(input("Enter account number: "))
            accounts = self.ui_controller.find_elements("navigation", "account_select")
            accounts[account_num].click()
            time.sleep(5)
        except IndexError:
            logging.error(f"No account found at index {account_num}.")
            self.ui_controller.close()

    def enter_parent_details(self, year_input: int) -> bool:
        result = True
        self.ui_controller.find_element("navigation", "parent_button").click()
        time.sleep(5)

        if self.ui_controller.wait_until("navigation", "next_button", timeout=15):
            self.ui_controller.find_element("navigation", "next_button").click()

        current_year = datetime.datetime.now().year
        numbers = [int(num) for num in str(year_input)]

        if (current_year - year_input) < 18:
            logging.error("You are not old enough to be a parent.")
            result = False
        else:
            for i in range(1, 5):
                if self.ui_controller.wait_until("age_gate", f"digit_{i}", timeout=20):
                    self.ui_controller.find_element("age_gate", f"digit_{i}").send_keys(numbers[i - 1])
                time.sleep(2)

        time.sleep(2)
        self.ui_controller.find_element("navigation", "submit_button").click()
        return result

    def video_stream(self):
        if self.ui_controller.wait_until("video", "video_stream", timeout=10):
            time.sleep(2)
            video_element = self.ui_controller.find_element("video", 'video_stream')
            video_duration = self.ui_controller.execute_script("return arguments[0].duration;", video_element)
            print(f"Video duration: {video_duration}")
            time.sleep(video_duration)

        if self.ui_controller.wait_until("navigation", "sign_in_info_next_button", timeout=10):
            self.ui_controller.find_element("navigation", "sign_in_info_next_button").click()
            time.sleep(5)

    def play_first_video(self, duration: int, email: str, password: str):
        result = True
        self.login_without_login(self.url)

        user_type = input('Select: child or parent: ')
        if user_type == 'parent':
            year_input = int(input('Please enter the year you were born in: '))
            self.enter_parent_details(year_input)
            time.sleep(5)

            self.video_stream()

            result &=self.login_(email, password)

            if result:
               if self.ui_controller.wait_until("navigation","bitti_button",timeout=20):
                  self.ui_controller.find_element("navigation","bitti_button").click()

               self.select_account()

               try:
                   result &= self.play_video(duration)
               except NoSuchElementException as e:
                   print(f"Error: {e}")
                   result = False

            else:
                result=False

            return result

        else:
            self.ui_controller.find_element("navigation", "child_button").click()
            print('Ask a parent to set up YouTubeKids')
            time.sleep(5)

            self.driver.quit()

    def login_without_login(self, url) -> bool:
        self.ui_controller.open_url(self.url)
        return True

    def play_video(self, duration)->bool:
        result = True
        if self.ui_controller.wait_until("video", "first_video", timeout=10):
           self.ui_controller.find_element("video", "first_video").click()
           time.sleep(duration)
        return result

    def login_(self, email: str, password: str) -> bool:
        result=True
        if self.ui_controller.wait_until("login", "login_button", timeout=20):
            self.ui_controller.find_element("login", "login_button").click()
        else:
            result = False

        original_window = self.ui_controller.current_window_handle()
        for handle in self.ui_controller.window_handles():
            if handle != original_window:
                self.ui_controller.switch_to_window(handle)
                break


        if self.ui_controller.wait_until("login", "email", timeout=10):
            self.ui_controller.find_element("login", "email").send_keys(email)

        if self.ui_controller.wait_until("login", "continue_button", timeout=10):
            self.ui_controller.find_element("login", "continue_button").click()

        time.sleep(2)

        if self.ui_controller.wait_until("login", "password", timeout=10):
            self.ui_controller.find_element("login", "password").send_keys(password)
        if self.ui_controller.wait_until("login", "login_button2", timeout=10):
            self.ui_controller.find_element("login", "login_button2").click()

        time.sleep(3)

        self.ui_controller.switch_to_window(original_window)

        return result

