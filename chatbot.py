import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

class InstagramBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        chrome_options = Options()
        # chrome_options.add_argument("--headless") # Uncomment if you don't need a browser UI
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.login()

    def login(self):
        self.driver.get("https://www.instagram.com/")
        time.sleep(2)
        username_input = self.driver.find_element(By.NAME, "username")
        password_input = self.driver.find_element(By.NAME, "password")

        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.RETURN)
        time.sleep(5)

        # Close pop-ups after login if necessary
        self.close_popups()

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

# Usage
bot = InstagramBot(your_username, your_password)
bot.check_unread_messages()
bot.close_browser()
