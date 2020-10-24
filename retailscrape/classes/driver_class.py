from selenium import webdriver # type: ignore
import os # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore

class Driver:
    def __init__(self):
        self.path = os.getcwd()
        self.chrome_dir = 'chromedriver'
        self.chrome_driver_filename = 'chromedriver.exe'
        self.chrome_driver_path = os.path.join(self.path, self.chrome_dir, self.chrome_driver_filename)
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--disable-logging')
        self.driver = webdriver.Chrome(executable_path=self.chrome_driver_path, options=self.chrome_options)
        self.wait_time = 20
        self.wait = WebDriverWait(self.driver, self.wait_time)