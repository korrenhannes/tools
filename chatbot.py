import time
import pickle
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv

class InstagramBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        chrome_options = Options()
        # chrome_options.add_argument("--headless") # Uncomment if you don't need a browser UI
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.cookies_file = "instagram_cookies.pkl"
        self.login()

    def login(self):
        self.driver.get("https://www.instagram.com/")
        if not self.load_cookies():
            time.sleep(2)
            username_input = self.driver.find_element(By.NAME, "username")
            password_input = self.driver.find_element(By.NAME, "password")

            username_input.send_keys(self.username)
            password_input.send_keys(self.password)
            password_input.send_keys(Keys.RETURN)
            time.sleep(5)

            # Save cookies after successful login
            self.save_cookies()

            # Close pop-ups after login if necessary
            self.close_popups()
        else:
            # Wait for page to load with cookies
            time.sleep(5)

    def save_cookies(self):
        with open(self.cookies_file, "wb") as file:
            pickle.dump(self.driver.get_cookies(), file)

    def load_cookies(self):
        try:
            with open(self.cookies_file, "rb") as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
            self.driver.refresh()
            return True
        except (FileNotFoundError, pickle.UnpicklingError):
            return False

    def close_popups(self):
        try:
            not_now_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]")
            not_now_button.click()
            time.sleep(2)
        except NoSuchElementException:
            pass

    def navigate_to_direct_messages(self):
        direct_message_icon = self.driver.find_element(By.XPATH, "//svg[@aria-label='Direct']")
        direct_message_icon.click()
        time.sleep(5)

    def check_unread_messages(self):
        self.navigate_to_direct_messages()
        chat_list = self.driver.find_elements(By.XPATH, "//div[@role='listitem']")
        for chat in chat_list:
            try:
                # Check for the unread element
                chat.find_element(By.XPATH, ".//div[contains(@class, 'x1a02dak')]")
                chat.click()  # Open the conversation
                time.sleep(2)
                # Add any interaction you want to have in the conversation here
                self.driver.back()  # Go back to the chat list
                time.sleep(2)
            except NoSuchElementException:
                continue

    def close_browser(self):
        self.driver.quit()

load_dotenv()
INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME')
INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD')

# Usage
bot = InstagramBot(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
bot.check_unread_messages()
bot.close_browser()
