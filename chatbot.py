import time
import pickle
import os
import openai
import random
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
            wait = WebDriverWait(self.driver, 10)
            # Updated XPath to match your provided HTML element
            direct_message_icon = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Direct messaging - 1 new notification link']")))
            direct_message_icon.click()
            time.sleep(5)
            return True
        except TimeoutException:
            print("Direct message icon not found or not clickable.")
            return False

    def check_unread_messages(self):
        if not self.navigate_to_direct_messages():
            print("Failed to navigate to direct messages.")
            return

        chat_list = self.driver.find_elements(By.XPATH, "//div[@role='listitem']")
        for chat in chat_list:
            try:
                # Check if the unread indicator element is present
                chat.find_element(By.XPATH, ".//span[contains(@class, 'x6s0dn4') and contains(@class, 'xzolkzo')]")
                chat.click()  # Open the conversation
                time.sleep(2)
                # Add any interaction you want to have in the conversation here
                self.driver.back()  # Go back to the chat list
                time.sleep(2)
            except NoSuchElementException:
                # If unread indicator not found, skip to the next chat
                continue

    def generate_message(self, prompt):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",  # or any other GPT-3.5 model
                prompt=prompt,
                max_tokens=50
            )
            return response.choices[0].text.strip()
        except Exception as e:
            print(f"Error in generating message: {e}")
            return None
        
    def respond_to_message(self, username, prompt):
        try:
            # Navigate to the user's profile and open the message box
            if not self.interact_with_profile(username):
                print(f"Could not interact with {username}'s profile.")
                return

            # Generate a message
            message = self.generate_message(prompt)
            if message:
                # Find the message input box and type the message
                message_box_selector = "div[contenteditable='true'][data-lexical-editor='true']"
                message_box = WebDriverWait(self.bot, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, message_box_selector)))
                ActionChains(self.bot).click(message_box).perform()
                for char in message:
                    ActionChains(self.bot).send_keys(char).perform()
                    time.sleep(random.uniform(0.1, 0.3))  # Random sleep between keystrokes

                # Send the message
                ActionChains(self.bot).send_keys(Keys.RETURN).perform()
                print(f"Message sent to {username}.")
            else:
                print("Failed to generate a message.")
        except Exception as e:
            print(f"Error responding to message for {username}: {e}")
    def close_browser(self):
        self.driver.quit()

load_dotenv()
INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME')
INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD')

# Usage
bot = InstagramBot(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
bot.check_unread_messages()
bot.close_browser()
