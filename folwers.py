from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
import string

class InstagramBot:
    def __init__(self, username, password, target_users):
        self.username = username
        self.password = password
        self.target_users = target_users
        self.driver = webdriver.Chrome()

    def close_browser(self):
        self.driver.close()

    def login(self):
        try:
            self.driver.get('https://www.instagram.com/accounts/login/')
            time.sleep(random.uniform(3, 5))

            username_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'username')))
            password_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'password')))

            username_input.send_keys(self.username)
            password_input.send_keys(self.password)
            password_input.send_keys(Keys.RETURN)

            time.sleep(random.uniform(5, 7))
        except Exception as e:
            print(f"Error during login: {e}")
            self.close_browser()

    def get_followers(self):
        followers = {}
        for user in self.target_users:
            try:
                self.driver.get(f'https://www.instagram.com/{user}/')
                time.sleep(random.uniform(2, 3))

                try:
                    followers_link = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'followers')))
                    followers_link.click()
                    time.sleep(random.uniform(2, 3))
                except Exception as e:
                    raise Exception(f"Unable to find or click on followers link for {user}: {e}")

                followers[user] = self.collect_usernames(user)
            except Exception as e:
                print(f"Error processing user {user}: {e}")

        return followers

    def extract_number_of_followers(self, user):
        try:
            followers_count_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//li[2]//span")))
            return int(followers_count_element.text.replace(',', ''))
        except Exception as e:
            print(f"Error extracting follower count for {user}: {e}")
            return 0

    def collect_usernames(self, user):
        alphabet = string.ascii_lowercase  # Gets all the letters in the alphabet
        all_followers = set()  # To store all unique followers

        try:
            print(f"Collecting followers for {user}")

            # Initial navigation to user's profile and open followers modal
            self.driver.get(f'https://www.instagram.com/{user}/')
            time.sleep(random.uniform(5, 8))
            followers_link = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'followers')))
            followers_link.click()
            time.sleep(random.uniform(5, 8))

            followers_modal = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']")))

            for letter in alphabet:
                # Find the search bar in the followers modal
                search_bar = followers_modal.find_element(By.XPATH, "//input[@aria-label='Search input']")
                action = ActionChains(self.driver)
                action.click(search_bar).perform()
                action.send_keys(Keys.CONTROL + "a").send_keys(Keys.BACKSPACE).perform()  # Clear search bar
                time.sleep(random.uniform(2, 4))
                action.send_keys(letter).perform()
                time.sleep(random.uniform(20, 25))  # Wait for search results to load

                last_height = self.driver.execute_script(
                    "return arguments[0].scrollHeight", followers_modal)

                while True:
                    self.driver.execute_script(
                        "arguments[0].scrollTop = arguments[0].scrollHeight", followers_modal)
                    time.sleep(random.uniform(8, 10))

                    # Collect usernames
                    followers_elements = followers_modal.find_elements(By.XPATH, "//a[contains(@class, '_a6hd')]/div/div/span")
                    print(f"Found {len(followers_elements)} followers elements for letter '{letter}'")

                    for element in followers_elements:
                        all_followers.add(element.text)

                    new_height = self.driver.execute_script(
                        "return arguments[0].scrollHeight", followers_modal)

                    if new_height == last_height:
                        break
                    last_height = new_height

                    if not followers_elements:
                        print(f"No new followers found for letter '{letter}'")
                        break

                    time.sleep(random.uniform(3, 5))

                # Pause before closing and reopening the modal
                time.sleep(random.uniform(2, 4))

            # Close the followers modal after all letters are processed
            close_button = followers_modal.find_element(By.XPATH, "//button[contains(@class, 'wpO6b')]")
            close_button.click()
            time.sleep(random.uniform(4, 6))

        except Exception as e:
            print(f"Error collecting usernames for {user}: {e}")

        return list(all_followers)


    def scroll_followers_modal(self, modal):
        last_height, current_height = 0, 1
        while last_height != current_height:
            last_height = current_height
            current_height = self.driver.execute_script(
                "arguments[0].scrollTo(0, arguments[0].scrollHeight); return arguments[0].scrollHeight;", modal)
            time.sleep(random.uniform(0.5, 1.0))


if __name__ == "__main__":
    USERNAME = 'joshclipit'
    PASSWORD = 'Kokoman10'
    TARGET_USERS = ['kindweirdwild', 'wordofmachine']

    bot = InstagramBot(USERNAME, PASSWORD, TARGET_USERS)
    bot.login()
    followers = bot.get_followers()
    bot.close_browser()

    with open("followers.txt", "w") as file:
        for user, usernames in followers.items():
            file.write(f"{user} followers ({len(usernames)}):\n")
            for username in usernames:
                file.write(username + "\n")
            file.write("\n")

    print("Followers have been written to followers.txt")
