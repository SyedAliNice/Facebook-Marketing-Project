import random
import os
import time
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os
import pyperclip







def get_credentials(id_filepath):
    credentials = []
    with open(id_filepath, "r") as file:
        for line in file:
            key, value = line.strip().split('=')
            if key == "username":
                credentials.append({"username": value})
            elif key == "password":
                credentials[-1]["password"] = value
    return credentials

def get_locations(location_file_path):
    with open(location_file_path, 'r') as file:
        locations = [line.strip() for line in file]
    return locations





def login_facebook(driver, credentials):
    driver.maximize_window()
    driver.get("https://www.facebook.com")
    time.sleep(2)
    driver.find_element(By.ID, "email").send_keys(credentials["username"])
    driver.find_element(By.ID, "pass").send_keys(credentials["password"])
    driver.find_element(By.NAME, "login").click()
    time.sleep(4)




def navigate_to_marketplace(driver):
    try:
        marketplace_button = driver.find_element(By.XPATH, "//span[text()='Marketplace']")
        marketplace_button.click()
        time.sleep(4)

    except Exception as e:
        print("Error navigating to Marketplace:", e)





def set_location(driver, location):
 
    try:
        # Clicking to open the location input field
        location_input_icon = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//i[@data-visualcompletion="css-img" and @class="x1b0d499 x1vv9jnp"]'))
        )
        location_input_icon.click()



                # Waiting for the input field
        inputting_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@aria-label='Location' and @role='combobox']"))
        )
        
        # Aggressive clear using JS and user simulation
        driver.execute_script("arguments[0].value = '';", inputting_button)  # Clearing via JS
        time.sleep(1)  # Small wait to let the UI sync
        
        inputting_button.send_keys("\ue003" * 20)  # Simulating multiple backspaces
        time.sleep(1)
        
        # Re-focus field and clearing again
        driver.execute_script("arguments[0].focus(); arguments[0].select();", inputting_button)
        inputting_button.clear()  # Clearing field natively again

        # Now inputing the desired location
        inputting_button.send_keys(location)
        time.sleep(2)  # Allowing the suggestion list to load



        # Waiting for the first suggestion in the dropdown and click it
        first_suggestion = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "(//div[@role='option'])[1]"))
        )
        first_suggestion.click()
        time.sleep(5)
        
        # Waiting for the "Apply" button and click it
        apply_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='none']//span[contains(text(), 'Apply')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", apply_button)
        apply_button.click()
        time.sleep(10)
        
        print("Location added successfully")
        
    except Exception as e:
        print("Error setting location:", e)







def process_account(credentials, location):
    options = webdriver.ChromeOptions()
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    
    options.add_argument('--headless')
    service = Service(ChromeDriverManager().install())
    #driver = webdriver.Chrome(service=service)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        print(f"Logging in as {credentials['username']} at location {location}")
        login_facebook(driver, credentials) 
        navigate_to_marketplace(driver)
        set_location(driver, location)
        
        time.sleep(5)

    except WebDriverException as e:
        print(f"Encountered an error with {credentials['username']}: {e}")
        time.sleep(5)  # Wait before retrying if necessary

    except WebDriverException as e:
        print(f"Encountered WebDriverException with {credentials['username']}: {e}")
       
    finally:
        driver.quit()



def open_facebook_marketplace_concurrently():
    credentials_list = get_credentials(id_filepath)
    locations = get_locations(location_file_path)
    
    # Asking the user for the number of concurrent tabs
    num_tabs = int(input("Enter the number of concurrent tabs to open: "))

    try:
        for i in range(0, len(credentials_list), num_tabs):
            threads = []
            batch_credentials = credentials_list[i:i + num_tabs]
            batch_locations = locations[i:i + num_tabs]

            for j, credentials in enumerate(batch_credentials):
                location = batch_locations[j % len(locations)]
                thread = threading.Thread(target=process_account, args=(credentials, location))
                threads.append(thread)
                thread.start()
                time.sleep(7)  # Adding delay to prevent rapid launches

            for thread in threads:
                thread.join()
    except:
        print("connection error")


if __name__ == "__main__":
    id_filepath = input("Path to IDs file: ")
    location_file_path = input("Enter location file path: ")

# Runing the function
open_facebook_marketplace_concurrently()
