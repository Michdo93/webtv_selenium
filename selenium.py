import sys
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import time
import pyautogui
from PIL import ImageGrab

pyautogui.FAILSAFE = False

class LiveStreamBot:
    def __init__(self, base_path, email, password, broadcaster):
        self.pyautogui_accuracy = 0.80
        self.base_path = base_path
        self.email = email
        self.password = password
        self.browser = None

        self.url = None
        self.accept_privacy_image = None

        self.login_form_xpath = None
        self.next_form_xpath = None
        self.login_xpath = None
        self.play_xpath = None
        self.fullscreen_xpath = None

        self.email_id = None
        self.password_id = None

        if broadcaster == "Kabel Eins":
            self.url = "https://video.kabeleins.de/livestreams/3"
            self.accept_privacy_image = 'accept_privacy_kabel_eins.PNG'
            self.login_form_xpath = '/html/body/div[1]/div/div[2]/div[1]/div[3]/div[4]/div/div[1]/div[1]/a'
            self.next_form_xpath = '//*[@id="root"]/div/div/div/div/div[2]/form/div/div[2]/button'
            self.login_xpath = '//*[@id="root"]/div/div/div/div/div[1]/div/div[2]/form/div/div[3]/div/div[1]/button'
            self.play_xpath = '//*[@id="video-in-container"]/div[2]/div/div[2]/div'
            self.fullscreen_xpath = '//*[@id="video-in-container"]/div[2]/div/div[3]/div/div/div[3]'
            self.email_id = "email"
            self.password_id = "password"
        elif broadcaster == "Kabel Eins Doku":
            self.url = "https://www.kabeleinsdoku.de/livestream"
            self.accept_privacy_image = 'accept_privacy_kabel_eins_doku.PNG'
            self.login_form_xpath = '//*[@id="main-content"]/div[3]/div[2]/div/div/div/div[1]/div[2]'
            self.next_form_xpath = '//*[@id="root"]/div/div/div/div/div[2]/form/div/div[2]/button'
            self.login_xpath = '//*[@id="root"]/div/div/div/div/div[1]/div/div[2]/form/div/div[3]/div/div[1]/button'
            self.play_xpath = '//*[@id="main-content"]/div[3]/div[2]/div/div/div/div[1]/div[2]'
            self.fullscreen_xpath = '//*[@id="video-in-container"]/div[2]/div/div[2]/div/div/div[2]/span'
            self.email_id = "email"
            self.password_id = "password"
        elif broadcaster == "ProSieben":
            self.url = "https://www.prosieben.de/livestream"
            self.accept_privacy_image = 'accept_privacy_prosieben.PNG'
            self.login_form_xpath = '//*[@id="root"]/div/div[2]/div[1]/div[3]/div[4]/div/div[1]/div[1]/a'
            self.next_form_xpath = '//*[@id="root"]/div/div/div/div/div[2]/form/div/div[2]/button'
            self.login_xpath = '//*[@id="root"]/div/div/div/div/div[1]/div/div[2]/form/div/div[3]/div/div[1]/button'
            self.play_xpath = '//*[@id="video-in-container"]/div[2]/div/div[2]/div'
            self.fullscreen_xpath = '//*[@id="video-in-container"]/div[2]/div/div[3]/div/div/div[3]/span'
            self.email_id = "email"
            self.password_id = "password"
        elif broadcaster == "ProSieben MAXX":
            self.url = "https://www.prosiebenmaxx.de/livestream"
            self.accept_privacy_image = 'accept_privacy_prosieben_maxx.PNG'
            self.login_form_xpath = '//*[@id="main-content"]/div[3]/div[2]/div/div/div/div[1]/div[2]'
            self.next_form_xpath = '//*[@id="root"]/div/div/div/div/div[2]/form/div/div[2]/button'
            self.login_xpath = '//*[@id="root"]/div/div/div/div/div[1]/div/div[2]/form/div/div[3]/div/div[1]/button'
            self.play_xpath = '//*[@id="main-content"]/div[3]/div[2]/div/div/div/div[1]/div[2]'
            self.fullscreen_xpath = '//*[@id="video-in-container"]/div[2]/div/div[3]/div/div/div[2]/span'
            self.email_id = "email"
            self.password_id = "password"
        elif broadcaster == "SAT.1":
            self.url = "https://video.sat1.de/livestreams/2"
            self.accept_privacy_image = 'accept_privacy_sat1.PNG'
            self.login_form_xpath = '//*[@id="root"]/div/div[2]/div[1]/div[3]/div[4]/div/div[1]/div[1]/a'
            self.next_form_xpath = '//*[@id="root"]/div/div/div/div/div[2]/form/div/div[2]/button'
            self.login_xpath = '//*[@id="root"]/div/div/div/div/div[1]/div/div[2]/form/div/div[3]/div/div[1]/button'
            self.play_xpath = '//*[@id="video-in-container"]/div[2]/div/div[2]/div'
            self.fullscreen_xpath = '//*[@id="video-in-container"]/div[2]/div/div[3]/div/div/div[3]/span'
            self.email_id = "email"
            self.password_id = "password"
        elif broadcaster == "SAT1.GOLD":
            self.url = "https://www.sat1gold.de/livestream"
            self.accept_privacy_image = 'accept_privacy_sat1_gold.PNG'
            self.login_form_xpath = '//*[@id="main-content"]/div[3]/div[2]/div/div/div/div[1]/div[2]'
            self.next_form_xpath = '//*[@id="root"]/div/div/div/div/div[2]/form/div/div[2]/button'
            self.login_xpath = '//*[@id="root"]/div/div/div/div/div[1]/div/div[2]/form/div/div[3]/div/div[1]/button'
            self.play_xpath = '//*[@id="main-content"]/div[3]/div[2]/div/div/div/div[1]/div[2]'
            self.fullscreen_xpath = '//*[@id="video-in-container"]/div[2]/div/div[2]/div/div/div[2]/span'
            self.email_id = "email"
            self.password_id = "password"
        elif broadcaster == "Sixx":
            self.url = "https://www.sixx.de/livestream"
            self.accept_privacy_image = 'accept_privacy_sixx.PNG'
            self.login_form_xpath = '//*[@id="root"]/div/div[2]/div[1]/div[3]/div[4]/div/div[1]/div[1]/a'
            self.next_form_xpath = '//*[@id="root"]/div/div/div/div/div[2]/form/div/div[2]/button'
            self.login_xpath = '//*[@id="root"]/div/div/div/div/div[1]/div/div[2]/form/div/div[3]/div/div[1]/button'
            self.play_xpath = '//*[@id="video-in-container"]/div[2]/div/div[2]/div'
            self.fullscreen_xpath = '//*[@id="video-in-container"]/div[2]/div/div[3]/div/div/div[3]/span'
            self.email_id = "email"
            self.password_id = "password"

    def __initialize_browser(self):
        if shutil.which("firefox") is not None:
            options = FirefoxOptions()
            options.add_argument("start-maximized")
            self.browser = webdriver.Firefox(options=options)
        elif shutil.which("chrome") is not None:
            options = Options()
            options.binary_location = shutil.which("chrome")
            options.chrome_driver_binary = shutil.which("chromedriver")
            options.add_argument("start-maximized")
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-notifications")
            options.add_argument("--accept-cookies")
            options.add_argument("--ignore-certificate-errors")
            self.browser = webdriver.Chrome(options=options)
        elif shutil.which("chromium-browser") is not None:
            options = Options()
            options.binary_location = shutil.which("chromium-browser")
            options.chrome_driver_binary = shutil.which("chromedriver")
            options.add_argument("start-maximized")
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument("--disable-gpu")
            self.browser = webdriver.Chrome(options=options)
        elif shutil.which("safari") is not None:
            options = SafariOptions()
            options.add_argument("start-maximized")
            self.browser = webdriver.Firefox(options=options)
        elif shutil.which("msedge") is not None:
            options = EdgeOptions()
            options.add_argument("start-maximized")
            self.browser = webdriver.Firefox(options=options)
        else:
            raise Exception("No supported browser found")

    def __accept_privacy_policy(self):
        accept_privacy = None
        timeout = time.time() + 3
        while accept_privacy is None and time.time() < timeout:
            try:
                accept_privacy = pyautogui.locateOnScreen(self.base_path + '/' + self.accept_privacy_image, confidence=self.pyautogui_accuracy)
            except Exception as e:
                print(e)
            if accept_privacy is not None:
                accept_privacy_center = pyautogui.center(accept_privacy)
                pyautogui.click(accept_privacy_center)
                break

    def login_and_play(self):
        self.__initialize_browser()

        self.browser.get(self.url)
        returned = "Page title was '{}'".format(self.browser.title)
        print(returned)

        time.sleep(5)
        self.__accept_privacy_policy()

        time.sleep(2)

        if self.login_form_xpath is not None:
            try:
                # Klicken Sie auf den Login-Link
                login_form_button = self.browser.find_element(By.XPATH, self.login_form_xpath)
                login_form_button.click()
                print("Login link clicked successfully.")
            except NoSuchElementException:
                print("Login link not found.")

            time.sleep(1)

        try:
            # Klicken Sie auf den Login-Link
            email_field = self.browser.find_element(By.ID, self.email_id)
            time.sleep(0.1)
            email_field.send_keys(self.email)
        except NoSuchElementException:
            print("Email field not found.")

        time.sleep(1)

        if self.next_form_xpath is not None:
            try:
                # Klicken Sie auf den Login-Link
                next_button = self.browser.find_element(By.XPATH, self.next_form_xpath)
                next_button.click()
                print("Email clicked successfully.")
            except NoSuchElementException:
                print("Email not found.")

            time.sleep(1)

        try:
            # Klicken Sie auf den Login-Link
            password_field = self.browser.find_element(By.ID, self.password_id)
            time.sleep(0.1)
            password_field.send_keys(self.password)
        except NoSuchElementException:
            print("Password field not found.")

        time.sleep(1)

        if self.login_xpath is not None:
            try:
                # Klicken Sie auf den Login-Link
                login_button = self.browser.find_element(By.XPATH, self.login_xpath)
                login_button.click()
                print("Login clicked successfully.")
            except NoSuchElementException:
                print("Login not found.")

            time.sleep(3)

        if self.play_xpath is not None:
            try:
                # Klicken Sie auf den Login-Link
                play_button = self.browser.find_element(By.XPATH, self.play_xpath)
                play_button.click()
                print("Play clicked successfully.")
            except NoSuchElementException:
                print("Play not found.")

            time.sleep(1)

        if self.fullscreen_xpath is not None:
            try:
                # Klicken Sie auf den Login-Link
                fullscreen_button = self.browser.find_element(By.XPATH, self.fullscreen_xpath)
                fullscreen_button.click()
                print("Fullscreen clicked successfully.")
            except NoSuchElementException:
                print("Fullscreen not found.")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Program terminated by user.")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        broadcast = str(sys.argv[1])
        bot = LiveStreamBot('<path/to/images/>', "<email>", "<password>", broadcast)
        bot.login_and_play()
