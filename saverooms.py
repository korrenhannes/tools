import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time  # Add this at the top where other imports are

# Initialize the WebDriver (using Chrome in this example)
driver = webdriver.Chrome()

# Open the specified URL
driver.get("https://schedule.tau.ac.il/scilib/Web/index.php")

your_username = "korrenh"  # Your username
your_password = "Kokoh102"  # Your password

try:
    # Wait for the username (email) field to be available and insert the username
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "email"))
    )
    username_field.send_keys(your_username)

    # Find the password field and insert the password
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(your_password)

    # Find the login button using the CSS selector and click it
    login_button = driver.find_element(By.CSS_SELECTOR, "button[name='login'][value='submit']")
    login_button.click()

    # Wait for some element on the next page to ensure login was successful
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "some_element_after_login"))  # Adjust the locator as needed
    )

    print("Login successful")

    # Wait for the reservable slots to be visible and store them in a list
    reservable_slots = WebDriverWait(driver, 20).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "td.reservable.clickres.slot"))
    )

    # Choose a random slot from the list
    chosen_slot = random.choice(reservable_slots)

    # Scroll to the chosen slot
    driver.execute_script("arguments[0].scrollIntoView(true);", chosen_slot)
    WebDriverWait(driver, 10).until(
        EC.visibility_of(chosen_slot)
    )

    # Wait for 10 seconds
    time.sleep(10)
    
    # Hover over the chosen slot before clicking
    ActionChains(driver).move_to_element(chosen_slot).perform()

    # Use JavaScript to click the chosen slot
    driver.execute_script("arguments[0].click();", chosen_slot)

    print("Reservable slot clicked")

    # Wait for the "Create" button to be clickable and click it
    create_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-success.save.create.btnCreate"))
    )
    create_button.click()

    print("Reservation created")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser window
    driver.quit()
