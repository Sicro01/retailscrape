from selenium import webdriver # type: ignore
import os # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from fake_useragent import UserAgent  # type: ignore


class Driver:
    def __init__(self):
        self.path = os.getcwd()
        self.chrome_dir = 'chromedriver'
        self.chrome_driver_filename = 'chromedriver.exe'
        self.chrome_driver_path = os.path.join(self.path, self.chrome_dir, self.chrome_driver_filename)
        self.user_agent = UserAgent()
        self.user_agent_random = self.user_agent.random
        self.chrome_options = webdriver.ChromeOptions()
        # self.chrome_options.add_argument('--disable-logging')
        self.chrome_options.add_argument('--log-level=3')
        self.chrome_options.add_argument(f'user-agent={self.user_agent_random}')
        self.chrome_options.add_argument('--disable-extensions')
        self.chrome_options.add_argument('--profile-directory=Default')
        self.chrome_options.add_argument('--incognito')
        self.chrome_options.add_argument('--disable-plugins-discovery')
        self.chrome_options.add_argument('--start-maximized')
        self.chrome_options.add_argument('--allow-insecure-localhost')
        self.chrome_options.add_argument('--ignore-certificate-errors')
        self.chrome_options.add_argument('--ignore-ssl-errors')
        self.chrome_options.add_argument('--ignore-certificate-errors-spki-list')
        self.driver = webdriver.Chrome(executable_path=self.chrome_driver_path, options=self.chrome_options)
        self.wait_time = 20
        self.wait = WebDriverWait(self.driver, self.wait_time)
        # self.driver.delete_all_cookies()
        self.driver.set_window_size(800,800)
        self.driver.set_window_position(0,0)
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
                })
            """
        })
        