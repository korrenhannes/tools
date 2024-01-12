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
import subprocess

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


        # Check and handle the second cookie dialog option
        try:
            decline_cookies_button = WebDriverWait(self.bot, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(@class, '_a9-- _ap36 _a9_1')]")))
            decline_cookies_button.click()
            print("Declined optional cookies using the second dialog option.")
            time.sleep(random.uniform(3, 5))  # Short pause after clicking
        except Exception as e:
            print(f"Second cookie dialog option not found. Error: {e}")


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
            # Navigate to Instagram's main page
            self.bot.get('https://www.instagram.com/')
            self.random_sleep(2, 5)

            # Hover over the search icon
            search_icon = WebDriverWait(self.bot, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[descendant::*[@aria-label='Search']]")))
            ActionChains(self.bot).move_to_element(search_icon).perform()
            self.random_sleep(1, 3)

            # Click the search icon to open search input
            search_icon.click()
            self.random_sleep(1, 3)

            # Find the search input element
            search_input = WebDriverWait(self.bot, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Search input']")))

            # Clear any existing text and type the username character by character
            ActionChains(self.bot).click(search_input).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).perform()
            for char in username:
                ActionChains(self.bot).send_keys_to_element(search_input, char).perform()
                time.sleep(random.uniform(0.1, 0.3))  # Random sleep between keystrokes

            self.random_sleep(2, 4)


            # Select the user from search suggestions
            profile_xpath = f"//a[contains(@href, '/{username}/')]"
            profile_link = WebDriverWait(self.bot, 10).until(
                EC.presence_of_element_located((By.XPATH, profile_xpath)))
            profile_link.click()
            self.random_sleep(3, 6)


            # Wait for the profile to load and ensure we are on the correct page
            WebDriverWait(self.bot, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//h2[text()='{username}']")))
            
            if not self.interact_with_profile(username):
                # Close the tab if interaction failed and continue with the next user
                continue

            # Scroll the page to mimic human behavior
            self.scroll_page()

            # Random sleep before closing the tab to simulate reading time
            self.random_sleep(3000, 4000)

        print("All messages sent.")

    def interact_with_profile(self, username):
        try:

            # Wait for the profile to fully load
            self.random_sleep(2, 4)

            # Locate and click the 'Follow' button
            follow_button_xpath = "//button[contains(@class, '_acan') and contains(., 'Follow')]"
            follow_button = WebDriverWait(self.bot, 10).until(
                EC.element_to_be_clickable((By.XPATH, follow_button_xpath)))
            follow_button.click()
            print(f"Clicked 'Follow' button for {username}.")
            self.random_sleep(2, 5)
            
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

    def run_shell_command(self, command):
        try:
            subprocess.run(command, shell=True)
        except Exception as e:
            print(f"Error running shell command: {e}")

    def prevent_sleep(self):
        # Runs the caffeinate command to prevent sleep
        self.run_shell_command("caffeinate -dimsu &")

    def allow_sleep(self):
        # Kills the caffeinate process to allow sleep again
        self.run_shell_command("pkill caffeinate")


def init():
    # Path to the file containing followers
    file_path = '/Users/korrenhannes/Desktop/random shit/followers.txt'
    users = read_followers_from_file(file_path)

    message_ = ("Hi,\n\n"
                "I came across your profile and noticed your interest in content creation. "
                "I’m Doron from ClipIt. We focus on making creativity simpler and more accessible for everyone.\n\n"
                "I’m curious, have you ever wanted to create engaging content for social media but found the process a bit daunting? "
                "We’re working on a tool that might help ease this process.\n\n"
                "Would you be interested in hearing a bit more about it? Your input would be really valuable to us.\n\n"
                "Thanks!")
    bot = Bot('doronytoto1232345', '2HLqF,B*vk!,h;x', users, message_)

    bot.prevent_sleep()

    input("DONE")

    bot.allow_sleep()


init()
