from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from base import WebDriverController
from discordpage import DiscordPage
from youtubekidspage import YoutubeKidsPage
from amazonvideo import AmazonVideoPage
from warnerturnerpage import WarnerturnerPage
from skypepage import SkypePage
import time

class ErrorHandling:
    @staticmethod
    def handle_exception(e):
        if isinstance(e, ValueError):
            print(f"ValueError occurred: {e}")
        elif isinstance(e, TimeoutException):
            print(f"TimeoutException occurred: {e}")
        elif isinstance(e, WebDriverException):
            print(f"WebDriverException occurred: {e}")
        else:
            print(f"Unexpected error occurred: {e}")

if __name__ == '__main__':
    web_driver_controller = WebDriverController()

    options = web_driver_controller.prepare_options(headless=False)
    web_driver_controller.open(driver_options=options)

    sites = {
        'Discord': ('discordpage.json', DiscordPage),
        'YoutubeKids': ('youtubekids.json', YoutubeKidsPage),
        'AmazonVideo': ('amazonvideo.json', AmazonVideoPage),
        'WarnerTurner':('warnerturner.json',WarnerturnerPage),
        'Skype':('skypepage.json',SkypePage)
    }

    try:
        site_name = input("Please enter the site name (Discord, YoutubeKids, AmazonVideo, WarnerTurner, Skype): ")
        config_file, site_class = sites.get(site_name, (None, None))

        if not site_class:
            print(f"Site '{site_name}' is not listed above")
            time.sleep(3)
            web_driver_controller.close()
            exit()

        page = site_class(web_driver_controller.driver, config_file)
        email = "gs1905-ayln@hotmail.com"
        password = "1905190512345"
        duration = int(input("Please enter the duration in seconds: "))

        if site_name in ('Discord', 'Skype'):
            page.start_video_call(duration, email, password)
        else:
            page.play_first_video(duration, email, password)

    except Exception as e:
        ErrorHandling.handle_exception(e)
