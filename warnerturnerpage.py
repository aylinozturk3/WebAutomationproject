from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from base import WebDriverController
import time

class WarnerturnerPage(WebDriverController):
    def __init__(self, driver, config_file):
        super().__init__(driver, config_file)
        self.url = 'https://press.wbd.com/us/'
        self.ui_controller = WebDriverController(driver, config_file)

    def play_first_video(self, duration, email, password)->bool:
        result=True
        self.login_without_login(self.url)

        if self.wait_until("login", "login_button", timeout=10):
            self.click("login", "login_button")
        else:
            print("Login button not found")
            return False

        self.login_(email, password)


        if self.wait_until("video", "menu", timeout=10):
            self.click("video", "menu")
        else:
            print("Menu item not found")
            return False

        time.sleep(3)

        divs = self.driver.find_elements(By.CSS_SELECTOR, self.config["video"]["brand_icon_list"]["path"])
        index = int(input("Enter the index of the div to click: "))
        if 0 <= index < len(divs):
            divs[index].click()
        else:
            print("Index out of range, please enter a valid index")
            return False

        if self.wait_until("video", "video_thumbnail", timeout=10):
            self.click("video", "video_thumbnail")
            time.sleep(5)
        else:
            print("Video thumbnail not found")
            return False
        try:
            result &=self.play_video(duration)

        except NoSuchElementException as e:
            print(f"Error: {e}")
            result = False

        return result

    def play_video(self, duration:int)->bool:
        result=True
        link_elements=self.ui_controller.find_elements("video","link_elements")

        if link_elements:
            actions = ActionChains(self.driver)
            actions.move_to_element(link_elements[0]).perform()
            time.sleep(2)
            link_elements[0].click()

            video_duration = self.driver.execute_script("return document.querySelector('video').duration;")
            print(f"Video duration: {video_duration} sec.")
            if duration < video_duration:
                starttime = time.time()
                while True:
                    currenttime = time.time()
                    elapsedtime = currenttime - starttime
                    if elapsedtime >= duration:
                        break
                time.sleep(duration)
                self.ui_controller.quit()
            else:
                time.sleep(video_duration)
        else:
            print("no video on the page")

        return result

    def login_without_login(self, url) -> bool:
        result = True
        self.open_url(self.url)

        return result


    def login_(self, email: str, password: str) -> bool:
        self.find_element("login", "email").send_keys(email)

        if self.wait_until("login", "password", timeout=10):
            self.find_element("login", "password").send_keys(password)

        if self.wait_until("login", "login_button2", timeout=5):
            self.find_element("login", "login_button2").click()

        return self.wait_until("login", "verify_element", timeout=20) is not None
