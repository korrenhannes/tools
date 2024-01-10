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

        # Send messages
        self.send_messages()

    def close_popups(self):
        time.sleep(5)  # Allow time for any popups to appear

        # Attempt to close the first pop-up
        instagram_logo_xpath = "//a[contains(@href, '/home') or contains(@href, '/')]"
        first_popup_closed = self.dismiss_popup(instagram_logo_xpath, "Instagram logo")

        # Attempt to close the second pop-up
        second_popup_selector = "//button[text()='Not Now']"  # Update if necessary
        second_popup_closed = self.dismiss_popup(second_popup_selector, "Not Now for second popup")

        # Return True if the first popup is closed and the second either closed or not found
        return first_popup_closed and (second_popup_closed or not second_popup_closed)

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

    def send_messages(self):
        if not self.close_popups():
            print("Failed to close all pop-ups. Cannot proceed to send messages.")
            return

        main_window_handle = self.bot.current_window_handle  # Save the handle of the main window

        for username in self.users:
            # Open a new tab with the user's profile page
            user_url = f'https://www.instagram.com/{username}/'
            self.bot.execute_script(f"window.open('{user_url}', '_blank');")
            time.sleep(2)

            # Switch to the new tab
            self.bot.switch_to.window(self.bot.window_handles[1])
            time.sleep(3)

            # Check for the presence of the message button and click it
            self.interact_with_profile(username)

            # Close the new tab and switch back to the main window
            self.bot.close()
            self.bot.switch_to.window(main_window_handle)

            # Wait a bit before processing the next user
            time.sleep(5)

    def interact_with_profile(self, username):
        # Interact with the user's profile in the new tab
        try:
            message_button_xpath = "//button[contains(text(),'Message') or contains(text(),'Send Message')]"
            message_button = WebDriverWait(self.bot, 10).until(
                EC.element_to_be_clickable((By.XPATH, message_button_xpath)))
            message_button.click()
            print(f"Opened message window for {username}.")

            # Type and send the message
            self.type_and_send_message(username)
        except Exception as e:
            print(f"Could not open message window for {username}. Error: {e}")

    def type_and_send_message(self, username):
        # Type and send the message in the DM window
        try:
            message_textarea_xpath = "//textarea[@placeholder='Message…']"
            message_box = WebDriverWait(self.bot, 20).until(
            EC.presence_of_element_located((By.XPATH, message_textarea_xpath)))
            message_box.send_keys(self.message)
            message_box.send_keys(Keys.RETURN)
            print(f"Message sent to {username}.")
        except Exception as e:
            print(f"Could not send message to {username}. Error: {e}")

def init():
    users = ['jlautman1', 'seanben_david']
    message_ = "final test"
    bot = Bot('korrenhannes', 'Kokoman10', users, message_)
    input("DONE")

init()