# importing module
from selenium import webdriver
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
 
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)


# enter receiver user name
user = ['User_name', 'User_name ']
message_ = ("final test")
 
 
class Bot:
    def __init__(self, username, password, users, message):
        self.username = username
        self.password = password
        self.users = users
        self.message = message
        self.bot = driver
        self.login()

    def login(self):
        self.bot.get('https://www.instagram.com/')
        enter_username = WebDriverWait(self.bot, 20).until(
            EC.presence_of_element_located((By.NAME, 'username')))
        enter_username.send_keys(self.username)
        enter_password = WebDriverWait(self.bot, 20).until(
            EC.presence_of_element_located((By.NAME, 'password')))
        enter_password.send_keys(self.password)
        enter_password.send_keys(Keys.RETURN)
        time.sleep(5)

        # Handling pop-ups after login
        self.close_popups()

        # Navigate to direct messages
        self.navigate_to_messages()

        # Send messages
        self.send_messages()

    def close_popups(self):
        time.sleep(5)  # Allow time for any popups to appear

        # First pop-up: Try clicking on the Instagram logo to close the pop-up
        instagram_logo_xpath = "//a[contains(@href, '/home') or contains(@href, '/')]"
        self.dismiss_popup(instagram_logo_xpath, "Instagram logo")

        # Second pop-up: Add the selector for the second pop-up you want to close
        # Replace 'second_popup_selector' with the actual selector for the second pop-up
        second_popup_selector = "//button[text()='Not Now']"  # This is an example selector
        self.dismiss_popup(second_popup_selector, "Not Now for second popup")

    def dismiss_popup(self, selector, name):
        try:
            # Wait for the element to be clickable
            element = WebDriverWait(self.bot, 10).until(
                EC.element_to_be_clickable((By.XPATH, selector)))
            element.click()
            print(f"Closed '{name}' popup.")
        except Exception as e:
            print(f"No '{name}' popup found. Error: {e}")

    def navigate_to_messages(self):
        WebDriverWait(self.bot, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[@href='/direct/inbox/']"))).click()
        time.sleep(2)

    def send_messages(self):
        for username in self.users:
            compose_button = WebDriverWait(self.bot, 20).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'wpO6b')]")))
            compose_button.click()
            time.sleep(2)

            to_field = WebDriverWait(self.bot, 20).until(
                EC.presence_of_element_located((By.NAME, 'queryBox')))
            to_field.send_keys(username)
            time.sleep(2)

            select_user = WebDriverWait(self.bot, 20).until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='button']//div[contains(text(), '" + username + "')]")))
            select_user.click()
            time.sleep(2)

            next_button = WebDriverWait(self.bot, 20).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Next')]")))
            next_button.click()
            time.sleep(2)

            message_box = WebDriverWait(self.bot, 20).until(
                EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Message…']")))
            message_box.send_keys(self.message)
            message_box.send_keys(Keys.RETURN)
            time.sleep(2)

            back_button = WebDriverWait(self.bot, 20).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/direct/inbox/')]")))
            back_button.click()
            time.sleep(2)

def init():
    users = ['User_name', 'User_name ']
    message_ = "final test"
    bot = Bot('korrenhannes', 'Kokoman10', users, message_)
    input("DONE")

init()