import random
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("window-size=1024,768")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)

# Function to calculate seconds until a given datetime
def seconds_until(target_datetime):
    now = datetime.datetime.now()
    wait_time = (target_datetime - now).total_seconds()
    return max(0, wait_time)  # Return 0 if the time is in the past


# Function to perform the room reservation
def reserve_room(driver, target_datetime):

    try:

        # Additional code to wait until the target datetime
        print(f"Waiting until {target_datetime} to make a reservation...")
        time.sleep(seconds_until(target_datetime))

        # Code to select the date one week from the target datetime
        one_week_later = target_datetime + datetime.timedelta(weeks=1)
        # Login
        username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
        username_field.send_keys(your_username)
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(your_password)
        login_button = driver.find_element(By.CSS_SELECTOR, "button[name='login'][value='submit']")
        login_button.click()


        # Wait for the schedule page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "page-schedule")))

        # Scroll to the top of the page before clicking the calendar button
        driver.execute_script("window.scrollTo(0, -100);")  # Scrolls above the top of the page
        time.sleep(1)  # Small pause to ensure the page has adjusted to the scroll

        driver.execute_script("document.body.style.zoom='90%'")
        time.sleep(1)  # Small pause to ensure the page has adjusted to the scroll

        top_element = driver.find_element(By.CSS_SELECTOR, "body")
        driver.execute_script("arguments[0].scrollIntoView(true);", top_element)
        time.sleep(1)  # Allow time for scrolling

        # Use JavaScript to directly click the calendar button
        calendar_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "calendar_toggle")))
        driver.execute_script("arguments[0].click();", calendar_button)


        # Calculate one week from today
        target_date = datetime.today() + timedelta(days=7)
        target_day = target_date.strftime("%d").lstrip('0')  # Remove leading zero for single digit days
        target_month = target_date.month - 1  # Adjust for zero-based indexing in JavaScript
        target_year = target_date.year

        # Construct the XPath for the target date, ensuring it's clickable
        date_xpath = f"//td[@data-handler='selectDay'][@data-month='{target_month}'][@data-year='{target_year}']/a[text()='{target_day}']"
        target_date_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, date_xpath)))

        # Use JavaScript to click the target date to avoid any potential overlay issues
        driver.execute_script("arguments[0].click();", target_date_element)


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

# Inputs for the target date and time
target_date_str = input("Enter the target date (YYYY-MM-DD): ")
target_time_str = input("Enter the target time (HH:MM): ")

# Parsing the input date and time
target_date = datetime.datetime.strptime(target_date_str, "%Y-%m-%d")
target_time = datetime.datetime.strptime(target_time_str, "%H:%M").time()
target_datetime = datetime.datetime.combine(target_date, target_time)

try:
    # Initialize WebDriver and open the target URL
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.get("https://schedule.tau.ac.il/scilib/Web/index.php")
    
    your_username = "korrenh"
    your_password = "Kokoh102"
    
    reserve_room(driver, target_datetime, your_username, your_password)
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    if driver:
        driver.quit()
