from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from base import WebDriverController
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import json
class WarnerturnerPage(WebDriverController):
    def __init__(self, driver, config_file):
        super().__init__(driver, config_file)
        self.url = 'https://press.wbd.com/us/'
        self.ui_controller = WebDriverController(driver, config_file)

    def play_first_video(self, duration, email, password) -> bool:
        """general structure of the warnerturnerpage.py"""
        result = True
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
            result &= self.play_video(duration)

        except NoSuchElementException as e:
            print(f"Error: {e}")
            result = False

        return result

    def play_video(self, duration: int) -> bool:
        """playing video and resultin in a dict that store data which related to video"""
        result = True
        results = []
        link_elements = self.ui_controller.find_elements("video", "link_elements")

        if link_elements:
            actions = ActionChains(self.driver)
            actions.move_to_element(link_elements[0]).perform()
            time.sleep(2)
            link_elements[0].click()
            time.sleep(2)

            video_duration = self.driver.execute_script("return document.querySelector('video').duration;")
            print(f"Video duration: {video_duration} sec.")

            if not self.open_stats_field(): #open stats field before starting to obtain stats
                print("Failed to open stats field")
                return False

            for i in range(duration):
                stats = self.get_stats()
                results.append(stats)
                time.sleep(1)

            print(results)
            time.sleep(3)
            self.ui_controller.close()

            self.save_results_to_json(results)
        else:
            print("No video on the page")
            result = False

        return result

    def login_without_login(self, url) -> bool:
        """getting url and open the site without login"""
        result = True
        self.open_url(self.url)
        return result

    def login_(self, email: str, password: str) -> bool:
        """login to account"""
        self.find_element("login", "email").send_keys(email)

        if self.wait_until("login", "password", timeout=10):
            self.find_element("login", "password").send_keys(password)

        if self.wait_until("login", "login_button2", timeout=5):
            self.find_element("login", "login_button2").click()

        return self.wait_until("login", "verify_element", timeout=20) is not None

    def open_stats_field(self) -> bool:
        """Open stats field."""
        result = True

        video_element = WebDriverWait(self.driver, timeout=20).until(
            EC.visibility_of_element_located(
                (By.XPATH, self.config["video"]["video_element"]["path"])
            )
        )
        actions = ActionChains(self.driver)
        actions.context_click(video_element).perform() #sağ tıklama işlemi

        try:
            stats_option = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, self.config["statistics"]["meraklisi_icin_istatistikler"]["path"]))
            )
            stats_option.click()
        except Exception as e:
            print(f"Failed to open stats field: {e}")
            result = False

        return result

    def get_stats(self) -> dict:
        """Get statistics related to a video."""
        connection_speed = self.ui_controller.find_element("statistics", "connection_speed").text
        network_activity = self.ui_controller.find_element("statistics", "network_activity").text
        buffer_health = self.ui_controller.find_element("statistics", "buffer_health").text

        date_time = datetime.now()
        formatted_time = date_time.strftime("%Y-%m-%d %H:%M:%S")

        stats_data = {
            "timestamp": formatted_time,
            "connection_speed": connection_speed,
            "network_activity": network_activity,
            "buffer_health":buffer_health
        }

        return stats_data

    def save_results_to_json(self, data:list,filename:str="video_datas.json") ->None:
        """ save the collected data to a JSON file"""
        with open(filename, 'w') as json_file:
            json.dump(data,json_file,indent=4)

        print(f"data is saved to {filename}")
