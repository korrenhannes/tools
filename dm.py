# importing module
import random
from selenium import webdriver
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)


# enter receiver user name
user = ['User_name', 'User_name ']

# Function to read followers from file
def read_followers_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    followers = []
    for line in lines:
        line = line.strip()
        if line and not line.endswith('followers (11):'):
            followers.append(line)
    return followers

# Path to the file containing followers
file_path = '/Users/korrenhannes/Desktop/random shit/followers.txt'
users = read_followers_from_file(file_path)

message_ = "final test"
 
 
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
        time.sleep(random.uniform(3, 5))  # Short pause after clicking


        try:
            decline_cookies_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Decline optional cookies')]")))
            decline_cookies_button.click()
            time.sleep(random.uniform(3, 5))  # Short pause after clicking
        except Exception as e:
            print(f"Optional cookies button not found or error clicking it: {e}")

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

    def random_sleep(self, min_seconds, max_seconds):
        time.sleep(random.uniform(min_seconds, max_seconds))

    def scroll_page(self):
        scroll_command = "window.scrollTo(0, document.body.scrollHeight);"
        self.bot.execute_script(scroll_command)
        self.random_sleep(2, 5)
        scroll_command = "window.scrollTo(0, -document.body.scrollHeight);"
        self.bot.execute_script(scroll_command)
        self.random_sleep(2, 5)

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

        main_window_handle = self.bot.current_window_handle

        for username in self.users:
            # Open a new tab with the user's profile page
            user_url = f'https://www.instagram.com/{username}/'
            self.bot.execute_script(f"window.open('{user_url}', '_blank');")
            self.random_sleep(3, 6)

            # Switch to the new tab
            self.bot.switch_to.window(self.bot.window_handles[1])
            self.random_sleep(2, 4)

            if not self.interact_with_profile(username):
                # Close the new tab if interaction failed and continue with the next user
                self.bot.close()
                self.bot.switch_to.window(main_window_handle)
                continue

            # Scroll the page to mimic human behavior
            self.scroll_page()

            # Close the new tab and switch back to the main window
            self.bot.close()
            self.bot.switch_to.window(main_window_handle)

            # Random sleep to avoid rapid sequential actions
            self.random_sleep(5, 10)

    def interact_with_profile(self, username):
        try:
            message_button_xpath = "//div[contains(@class, 'x1i10hfl') and contains(text(), 'Message')]"
            message_button = WebDriverWait(self.bot, 10).until(
                EC.element_to_be_clickable((By.XPATH, message_button_xpath)))
            message_button.click()
            print(f"Clicked on message button for {username}. Waiting for message window to stabilize...")
            self.random_sleep(5, 10) # Wait for the message window to be fully loaded
            return self.type_and_send_message(username)
        except Exception as e:
            print(f"Could not interact with {username}'s profile. Error: {e}")
            return False

    def type_and_send_message(self, username):
        try:
            message_input_selector = "div[contenteditable='true'][data-lexical-editor='true']"
            message_box = WebDriverWait(self.bot, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, message_input_selector)))
            print(f"Attempting to send message to {username}...")

            # Clear the message box before typing
            ActionChains(self.bot).click(message_box).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).perform()

            # Type the message character by character
            for char in self.message:
                ActionChains(self.bot).send_keys_to_element(message_box, char).perform()
                time.sleep(random.uniform(0.1, 0.3))  # Random sleep between keystrokes

            # Send the message
            ActionChains(self.bot).send_keys_to_element(message_box, Keys.RETURN).perform()
            print(f"Message sent to {username}.")
            return True
        except Exception as e:
            print(f"Error sending message to {username}: {e}")
            return False

def init():
    # Path to the file containing followers
    file_path = '/Users/korrenhannes/Desktop/random shit/followers.txt'
    users = read_followers_from_file(file_path)

    message_ = "final test"
    bot = Bot('dandanrtk12312234', 'd0!wpFTYXqyZzfPM4!zY', users, message_)
    input("DONE")

init()
