from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

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

                try:
                    followers_list = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']//ul")))
                    number_of_followers = self.extract_number_of_followers(user)
                except Exception as e:
                    raise Exception(f"Unable to locate followers list for {user}: {e}")

                print(f"Collecting {number_of_followers} followers of {user}")
                followers[user] = self.collect_usernames(followers_list, number_of_followers)
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

    def collect_usernames(self, followers_list, number_of_followers):
        last_height, current_height = 0, 1
        scroll_pause = random.uniform(0.5, 1.0)
        usernames = set()

        while len(usernames) < number_of_followers:
            try:
                self.driver.execute_script(
                    "arguments[0].scrollTo(0, arguments[0].scrollHeight);", followers_list)
                time.sleep(scroll_pause)

                current_usernames = followers_list.find_elements(
                    By.XPATH, "//span[contains(@class, '_ap3a') and contains(@class, '_aaco')]")

                for username_element in current_usernames:
                    username = username_element.text
                    if username:
                        usernames.add(username)

                print(f"Found {len(usernames)} unique usernames so far.")

                last_height = current_height
                current_height = self.driver.execute_script(
                    "return arguments[0].scrollHeight;", followers_list)

                if last_height == current_height:
                    break
            except Exception as e:
                print(f"Error during scrolling: {e}")
                break

        return list(usernames)


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