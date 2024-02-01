import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # Maximize the window to ensure all elements are visible
driver = webdriver.Chrome(options=options)

# Open the target URL
driver.get("https://schedule.tau.ac.il/scilib/Web/index.php")

your_username = "korrenh"
your_password = "Kokoh102"

try:
    # Login
    username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
    username_field.send_keys(your_username)
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(your_password)
    login_button = driver.find_element(By.CSS_SELECTOR, "button[name='login'][value='submit']")
    login_button.click()

    # Wait for the schedule page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "page-schedule")))

    # Locate the schedule container
    schedule_container = driver.find_element(By.ID, "page-schedule")

    # Collect all reservable slots within the schedule container
    reservable_slots = schedule_container.find_elements(By.CSS_SELECTOR, "td.reservable.clickres.slot")

    # Filter out past slots if necessary and select a random slot
    future_slots = [slot for slot in reservable_slots if "pasttime" not in slot.get_attribute("class")]
    if not future_slots:
        raise Exception("No future slots available")
    chosen_slot = random.choice(future_slots)

    # Ensure the chosen slot is visible
    driver.execute_script("arguments[0].scrollIntoView(true);", chosen_slot)
    time.sleep(2)  # Allow time for any animations or dynamic content

    # Click the chosen slot
    ActionChains(driver).move_to_element(chosen_slot).click(chosen_slot).perform()

    # Confirm the reservation by clicking the "Create" button, ensure it's visible and clickable
    create_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-success.save.create.btnCreate"))
    )
    create_button.click()

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the browser after a short delay for observation
    time.sleep(5)  # Time to observe the last action, adjust as needed
    driver.quit()
