# importing module
import random
from selenium import webdriver
from fake_useragent import UserAgent
import os
import pickle
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent
from dotenv import load_dotenv
import subprocess
import selenium

print(selenium.__version__)

options = webdriver.ChromeOptions()

# Set random user-agent
options.add_argument(f'user-agent={UserAgent().random}')


# Update this path to the location where you have unzipped the proxy authentication extension
unzipped_proxy_auth_plugin_path = '/Users/korrenhannes/Desktop/random shit/proxy_auth_plugin/prox/Archive'

# Add the proxy authentication extension
options.add_argument(f'--load-extension={unzipped_proxy_auth_plugin_path}')


proxy_host = 'gate.smartproxy.com'
proxy_port = '10001'
options.add_argument(f'--proxy-server={proxy_host}:{proxy_port}')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


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
        self.messaged_users = []  # Add this line
        self.username = username
        self.password = password
        self.users = users
        self.message = message
        self.bot = driver
        self.cookies_file = "cookies.pkl"  # Define the path to save cookies
        self.login()


    def save_cookies(self):
        with open(self.cookies_file, "wb") as file:
            pickle.dump(self.bot.get_cookies(), file)
        print("Cookies saved.")

    def load_cookies(self):
        try:
            with open(self.cookies_file, "rb") as file:
                cookies = pickle.load(file)
                if not cookies:  # Check if the cookies list is empty
                    print("No cookies found in the file.")
                    return False
                for cookie in cookies:
                    self.bot.add_cookie(cookie)
            return True
        except (FileNotFoundError, EOFError) as e:
            print(f"Error loading cookies: {e}")
            return False

    def is_logged_in(self):
        # Modify this function to check for a specific element that indicates a logged-in state
        try:
            WebDriverWait(self.bot, 20).until(
                EC.presence_of_element_located((By.XPATH, "//span[descendant::*[@aria-label='Search']]")))
            return True
        except TimeoutException:
            return False
        
    def login(self):
        self.bot.get('https://www.instagram.com/')
        time.sleep(random.uniform(3, 5))  # Short pause after clicking


        # Try loading cookies if they exist
        if self.load_cookies():
            self.bot.get('https://www.instagram.com/')
            if self.is_logged_in():
                print("Logged in using cookies.")

                # Handling pop-ups after login
                self.close_popups()

                # Send messages
                self.send_messages()


                return
            else:
                print("Failed to log in with cookies. Proceeding with regular login.")

        try:
            decline_cookies_button = WebDriverWait(self.bot, 20).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Decline optional cookies')]")))
            self.click_element(decline_cookies_button)
            time.sleep(random.uniform(3, 5))  # Short pause after clicking
        except Exception as e:
            print(f"Optional cookies button not found or error clicking it: {e}")


        # Check and handle the second cookie dialog option
        try:
            decline_cookies_button = WebDriverWait(self.bot, 20).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(@class, '_a9-- _ap36 _a9_1')]")))
            self.click_element(decline_cookies_button)
            print("Declined optional cookies using the second dialog option.")
            time.sleep(random.uniform(3, 5))  # Short pause after clicking
        except Exception as e:
            print(f"Second cookie dialog option not found. Error: {e}")

        enter_username = WebDriverWait(self.bot, 20).until(
            EC.presence_of_element_located((By.NAME, 'username')))
        # Type the username letter by letter
        for char in self.username:
            enter_username.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))  # Random sleep between keystrokes

        enter_password = WebDriverWait(self.bot, 20).until(
            EC.presence_of_element_located((By.NAME, 'password')))
        # Type the password letter by letter
        for char in self.password:
            enter_password.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))  # Random sleep between keystrokes

        time.sleep(random.uniform(10, 15))  # Random sleep between keystrokes

        enter_password.send_keys(Keys.RETURN)
        time.sleep(5)

        self.save_cookies()

        # Handling pop-ups after login
        self.close_popups()

        # Send messages
        self.send_messages()

    def random_sleep(self, min_seconds, max_seconds):
        mean_sleep_time = (min_seconds + max_seconds) / 2  # Calculate the mean
        sigma = (max_seconds - min_seconds) / 6  # Calculate standard deviation for a reasonable spread
        sleep_time = random.gauss(mean_sleep_time, sigma)
        sleep_time = max(min_seconds, min(sleep_time, max_seconds))  # Ensure sleep time is within the given range
        time.sleep(sleep_time)

    def scroll_page(self):
        scroll_command = "window.scrollTo(0, document.body.scrollHeight);"
        self.bot.execute_script(scroll_command)
        self.random_sleep(2, 5)
        scroll_command = "window.scrollTo(0, -document.body.scrollHeight);"
        self.bot.execute_script(scroll_command)
        self.random_sleep(2, 5)

    def close_popups(self):
        try:
            # Second pop-up
            not_now_button = WebDriverWait(self.bot, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='Not Now']")))
            self.click_element(not_now_button)
            print("Closed 'Not Now for second popup' popup.")
        except TimeoutException:
            print("No 'Not Now for second popup' popup found.")

        try:
            # First pop-up
            insta_logo_button = WebDriverWait(self.bot, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/home') or contains(@href, '/')]")))
            self.click_element(insta_logo_button)

            print("Closed 'Instagram logo' popup.")
        except TimeoutException:
            print("No 'Instagram logo' popup found.")

        # Return True if the first popup is closed and the second either closed or not found
        return True

    def dismiss_popup(self, selector, name):
        try:
            element = WebDriverWait(self.bot, 30).until(
                EC.element_to_be_clickable((By.XPATH, selector)))
            self.bot.execute_script("arguments[0].scrollIntoView();", element)
            self.random_mouse_movement()  # Adding random mouse movement
            self.click_element(element)   # Using custom click function
            print(f"Closed '{name}' popup.")
            return True
        except Exception as e:
            print(f"No '{name}' popup found. Error: {e}")
            return False

    def send_messages(self):
        if not self.close_popups():
            print("Failed to close all pop-ups. Cannot proceed to send messages.")
            return


        message_count = 0

        main_window_handle = self.bot.current_window_handle

        for username in self.users:

            message_count += 1
            if message_count % 5 == 0:
                print("Calling external script after 3 messages...")
                self.call_external_script()

            # Navigate to Instagram's main page
            self.bot.get('https://www.instagram.com/')
            self.random_sleep(2, 5)

            self.random_mouse_movement()
            self.scroll_like_human()

            # Hover over the search icon
            search_icon = WebDriverWait(self.bot, 30).until(
                EC.presence_of_element_located((By.XPATH, "//span[descendant::*[@aria-label='Search']]")))
            ActionChains(self.bot).move_to_element(search_icon).perform()
            self.random_sleep(1, 3)

            # Click the search icon to open search input
            self.click_element(search_icon)

            self.random_sleep(1, 3)

            self.random_mouse_movement()
            self.scroll_like_human()
            self.random_sleep(1, 3)

            # Find the search input element
            search_input = WebDriverWait(self.bot, 30).until(
                EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Search input']")))

            # Clear any existing text and type the username character by character
            ActionChains(self.bot).click(search_input).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).perform()
            for char in username:
                ActionChains(self.bot).send_keys_to_element(search_input, char).perform()
                time.sleep(random.uniform(0.1, 0.3))  # Random sleep between keystrokes

            self.random_sleep(2, 4)


            # Select the user from search suggestions
            profile_xpath = f"//a[contains(@href, '/{username}/')]"
            profile_link = WebDriverWait(self.bot, 30).until(
                EC.presence_of_element_located((By.XPATH, profile_xpath)))
            self.click_element(profile_link)

            self.random_sleep(3, 6)


            # Wait for the profile to load and ensure we are on the correct page
            WebDriverWait(self.bot, 30).until(
                EC.presence_of_element_located((By.XPATH, f"//h2[text()='{username}']")))
            

            self.random_sleep(5, 10)
            self.random_mouse_movement()
            self.scroll_like_human()


            self.messaged_users.append(username)

            if not self.interact_with_profile(username, message_count):
                # Close the tab if interaction failed and continue with the next user
                continue

            # Scroll the page to mimic human behavior
            self.scroll_page()

            # Random sleep before closing the tab to simulate reading time
            self.random_sleep(3, 4)


            self.random_sleep(3, 4)


        print("All messages sent.")


    def call_external_script(self):
        try:
            result = subprocess.run(['python', '/Users/korrenhannes/Desktop/random shit/chatbot.py'], check=True, capture_output=True, text=True)
            print("External script output:", result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running the external script: {e}")
            print("Script output:", e.output)
            print("Script stderr:", e.stderr)

    def interact_with_profile(self, username, message_count):
        try:

            # Wait for the profile to fully load
            self.random_sleep(2, 4)

            # Locate and click the 'Follow' button
            follow_button_xpath = "//button[contains(@class, '_acan') and contains(., 'Follow')]"
            follow_button = WebDriverWait(self.bot, 30).until(
                EC.element_to_be_clickable((By.XPATH, follow_button_xpath)))
            self.bot.execute_script("arguments[0].scrollIntoView(true);", follow_button)
            self.random_mouse_movement()
            self.click_element(follow_button)
            print(f"Clicked 'Follow' button for {username}.")
            self.random_sleep(2, 5)
            
            message_button_xpath = "//div[contains(@class, 'x1i10hfl') and contains(text(), 'Message')]"
            message_button = WebDriverWait(self.bot, 30).until(
                EC.element_to_be_clickable((By.XPATH, message_button_xpath)))
            self.bot.execute_script("arguments[0].scrollIntoView(true);", message_button)
            self.random_mouse_movement()
            self.click_element(message_button)
            print(f"Clicked on message button for {username}. Waiting for message window to stabilize...")
            self.random_sleep(5, 10) # Wait for the message window to be fully loaded
            self.scroll_like_human()
            return self.type_and_send_message(username)
        except Exception as e:
            print(f"Could not interact with {username}'s profile. Error: {e}")
            message_count += 1
            return False

    def type_and_send_message(self, username):
        self.messaged_users.append(username)  # Append after successful sending

        try:
            message_input_selector = "div[contenteditable='true'][data-lexical-editor='true']"
            message_box = WebDriverWait(self.bot, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, message_input_selector)))
            print(f"Attempting to send message to {username}...")

            # Clear the message box before typing
            ActionChains(self.bot).click(message_box).perform()

            # Split the message into lines and type each line
            lines = self.message.split('\n')
            for i, line in enumerate(lines):

                for char in line:
                    ActionChains(self.bot).send_keys(char).perform()
                    time.sleep(random.uniform(0.1, 0.3))  # Random sleep between keystrokes
                
                if i < len(lines) - 1:  # If not the last line, add a newline
                    ActionChains(self.bot).key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT).perform()
                    time.sleep(random.uniform(0.1, 0.3)) # Sleep after adding a newline



            # Send the message
            ActionChains(self.bot).send_keys(Keys.RETURN).perform()
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
        # Starts the caffeinate process
        self.caffeinate_process = subprocess.Popen(["caffeinate", "-dimsu"])
        print("Preventing sleep mode.")

    def allow_sleep(self):
        # Terminates the caffeinate process
        if self.caffeinate_process:
            self.caffeinate_process.terminate()
            print("Allowing sleep mode.")

    def human_like_sleep(self, avg_duration, deviation):
        sleep_time = abs(random.normalvariate(avg_duration, deviation))
        time.sleep(sleep_time)

    def random_mouse_movement(self):
        action = ActionChains(self.bot)
        # Simulate a more complex path
        for _ in range(random.randint(3, 6)):
            x_offset = random.randint(-10, 10)
            y_offset = random.randint(-10, 10)
            action.move_by_offset(x_offset, y_offset).perform()
            self.random_sleep(1, 2)

    def click_element(self, element):
        try:
            # Ensure the element is in the viewport
            self.bot.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'nearest'});", element)
            self.random_sleep(1, 2)  # Adding a brief pause after scrolling

            # Check if element is visible and clickable
            if element.is_displayed() and element.is_enabled():
                action = ActionChains(self.bot)
                action.move_to_element(element).click().perform()
            else:
                print(f"Element not visible or not enabled: {element}")
        except Exception as e:
            print(f"Error clicking element: {e}")


    def scroll_to_element(self, element):
        try:
            # Scroll smoothly to the element, centering it in the viewport
            self.bot.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'nearest'});", element)
            self.random_sleep(1, 2)  # Pause after scrolling to allow for any lazy-loaded content
        except Exception as e:
            print(f"Error scrolling to element: {e}")

    def type_like_human(element, text):
        for char in text:
            time.sleep(random.uniform(0.05, 0.2))  # Mimic human typing speed
            element.send_keys(char)

    def scroll_like_human(self):
        body_element = self.bot.find_element(By.TAG_NAME, 'body')
        for _ in range(random.randint(2, 6)):
            scroll_direction = random.choice([Keys.PAGE_UP, Keys.PAGE_DOWN, Keys.ARROW_UP, Keys.ARROW_DOWN])
            body_element.send_keys(scroll_direction)
            self.human_like_sleep(1, 0.5)

class BotContextManager:
    def __init__(self, bot):
        self.bot = bot

    def __enter__(self):
        self.bot.prevent_sleep()
        return self.bot

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.bot.allow_sleep()


load_dotenv()
INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME')
INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD')


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

    bot = None
    try:
        bot = Bot(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD, users, message_)
        bot.prevent_sleep()
        bot.send_messages()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if bot is not None:
            bot.allow_sleep()
            # Update the file with the users who have not been messaged
            remaining_users = [user for user in users if user not in bot.messaged_users]
            with open(file_path, 'w') as file:
                for user in remaining_users:
                    file.write(user + '\n')
            print("Updated the file with remaining users.")
        else:
            print("Bot was not properly initialized.")


# Call the init function
init()
