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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
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

            self.close_popups()

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
        time.sleep(2)  # Wait a bit for any popups to load
        try:
            # Close 'Save Login Info' Popup if it appears
            save_info_popup = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='Not Now']")))
            save_info_popup.click()
            print("Closed 'Save Login Info' popup.")
        except TimeoutException:
            print("No 'Save Login Info' popup found.")

        try:
            # Close 'Turn on Notifications' Popup if it appears
            notifications_popup = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='Not Now']")))
            notifications_popup.click()
            print("Closed 'Turn on Notifications' popup.")
        except TimeoutException:
            print("No 'Turn on Notifications' popup found.")


    def dismiss_popup(self, selector, name):
        try:
            element = WebDriverWait(self.bot, 10).until(
                EC.element_to_be_clickable((By.XPATH, selector)))
            element.click()
            print(f"Closed '{name}' popup.")
            return True
        except Exception as e:
            print(f"No '{name}' popup found. Error: {e}")
            return False

    def navigate_to_direct_messages(self):
        try:
            wait = WebDriverWait(self.driver, 15)
            direct_message_icon = wait.until(EC.element_to_be_clickable((By.XPATH, "//nav//a[contains(@href, '/direct/inbox/')]")))
            direct_message_icon.click()
            time.sleep(5)
            return True
        except TimeoutException:
            print("Direct message icon not found or not clickable.")
            return False

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
