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




# Defining the path to the CSV file
csv_file = r"C:\Users\NEC\Desktop\Facebook Marketing Project\sofa_campain.csv"

# Creating a DataFrame if the file doesn't exist, otherwise load it
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
else:
    df = pd.DataFrame(columns=["campain_name", "title_file", "min_price", "max_price", "condition", "discription", "tags", "category_choice", "id_filepath", "location_file_path", "images_folder"])  # Adjust columns as needed


id_filepath = None
location_file_path = None

# Function to capture and save inputs to the CSV
def capture_inputs():
    global df
    campain_name = input("Enter Campaign Name: ")  # Unique identifier
    title_file = input("Path to Title: ")
    min_price = input("Enter Min Price: ")
    max_price = input("Enter Max Price: ")
    condition_choice = input("Enter Condition: ")
    description_file = input("Path to Description: ")
    product_tags = input("Enter Tags: ")
    category_choice = input("Enter Category in Number: ")
    id_filepath = input("Enter IDs path: ")
    location_file_path = input("Enter location path: ")
    images_folder = input("Enter image folder path: ")

    # Appending the new inputs as a new row to the DataFrame
    new_data = pd.DataFrame({
        "campain_name": [campain_name],  # Adding unique identifier column
        "title_file": [title_file],
        "min_price": [min_price],
        "max_price": [max_price],
        "condition": [condition_choice],
        "discription": [description_file],
        "tags": [product_tags],
        "category_choice": [category_choice],
        "id_filepath": [id_filepath],
        "location_file_path": [location_file_path],
        "images_folder": [images_folder]
    })
    df = pd.concat([df, new_data], ignore_index=True)
    
    # Saving the updated DataFrame to the CSV
    df.to_csv(csv_file, index=False)
    print("Inputs saved to CSV.")

# Function to load inputs by campaign name
def load_inputs_by_name(campain_name):
    global df
    if campain_name in df['campain_name'].values:
        inputs = df[df['campain_name'] == campain_name].iloc[0]  # Getting the first match
        print("Loaded inputs:", inputs.to_dict())
        
        # Assign values to variables
        title_file = inputs["title_file"]
        min_price = inputs["min_price"]
        max_price = inputs["max_price"]
        condition_choice = inputs["condition"]
        description_file = inputs["discription"]
        product_tags = inputs["tags"]
        category_choice = inputs["category_choice"]
        id_filepath = inputs["id_filepath"]
        location_file_path = inputs["location_file_path"]
        images_folder = inputs["images_folder"]
        
        # Return values
        return title_file, min_price, max_price, condition_choice, description_file, product_tags, category_choice, id_filepath, location_file_path, images_folder
    else:
        print("Campaign name not found!")
        return None, None, None

# Main flow for choosing input mode
choice = input("Do you want to (1) Enter new inputs or (2) Load from CSV by campaign name? Enter 1 or 2: ")

if choice == '1':
    capture_inputs()
elif choice == '2':
    campain_name = input("Enter the campaign name to load: ")
    title_file, min_price, max_price, condition_choice, description_file, product_tags, category_choice, id_filepath, location_file_path, images_folder = load_inputs_by_name(campain_name)
else:
    print("Invalid choice.")









def get_credentials():
    credentials = []
    with open(id_filepath, "r") as file:
        for line in file:
            key, value = line.strip().split('=')
            if key == "username":
                credentials.append({"username": value})
            elif key == "password":
                credentials[-1]["password"] = value
    return credentials

def get_locations():
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
        post_creation(driver)
        
        time.sleep(5)

    except WebDriverException as e:
        print(f"Encountered an error with {credentials['username']}: {e}")
        time.sleep(5)  # Wait before retrying if necessary

    except WebDriverException as e:
        print(f"Encountered WebDriverException with {credentials['username']}: {e}")
       
    finally:
        driver.quit()





def post_creation(driver):
    #clicking on the new listing button
    create_listing_button = driver.find_element(By.XPATH, "//span[text()='Create new listing' or text()='Sell Something']")
    create_listing_button.click()
    time.sleep(4)
    #clicking on item for sale button
    item_for_sale = driver.find_element(By.XPATH, "//i[@data-visualcompletion='css-img' and contains(@class, 'x3ajldb') and contains(@class, 'x14yjl9h')]")
    item_for_sale.click()
    time.sleep(4)

    
    try:
        # Locating the "Add photos" button
        image_input = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Add photos') and ancestor::div[contains(@class, 'x9f619') and contains(@class, 'x1n2onr6')]]"))
    )
    
    # Geting image paths from the folder
        image_paths = [os.path.join(images_folder, img) for img in os.listdir(images_folder)]
    
    # Checking if there are images to upload
        if image_paths:
        # Clicking on "Add photos" button (you can skip this if you directly access the file input)
            driver.execute_script("arguments[0];", image_input)

        # Locate the file input field
            file_input = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
        )
        
        # Upload the first image only
            file_input.send_keys(image_paths[0])
        
            print("Image uploaded successfully.")
        else:
            print("No images found in the specified folder.")

    except Exception as e:
        print("Error uploading image:", e)
    time.sleep(2)



    try:
        with open(title_file, "r", encoding='utf-8') as file:
            titles = [line.strip() for line in file if line.strip()]  # Only non-empty lines

        # Pick a title at random or sequentially based on preference
        title = random.choice(titles)  # or titles[0] for the first title
        title_box = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//label[@aria-label='Title']//input"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", title_box)
        #driver.execute_script("arguments[0].value = '';", title_box)  # Clear field
        title_box.send_keys(title)
        #driver.execute_script("arguments[0].value = arguments[1];", title_box, title)
        print(f"Title '{title}' added successfully.")
    except Exception as e:
        print("Error adding title:", e)   
    time.sleep(2)  


    

    try:
        # Generating a random price within the specified range
        price = random.randint(min_price, max_price)

        price_box = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'Price')]/following::input[@type='text'][1]"))
    )

        price_box.send_keys(price)  # Entering the price 
        print("Price added successfully.")
    except Exception as e:
        print("Error adding price:", e)
    time.sleep(2)



    # Adding condition to the post
    try:
        print("Select the condition for the item: 1 = New, 2 = Good, 3 = Used")
        condition_map = {"1": "New", "2": "Good", "3": "Used"}
        selected_condition = condition_map.get(condition_choice)

        condition_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@aria-haspopup="listbox" and @aria-expanded="false"]'))
        )
        condition_box.click()

        print(selected_condition)
        print(condition_choice)

        if condition_choice == 1:
            # Waiting for the specific option to be visible
            condition_option_new = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@role='option' and contains(@class, 'x1i10hfl') and contains(., 'New')]"))
            )
            condition_option_new.click()
            print("New condition selected.")
        
        elif condition_choice == 2:
            # Waiting for the specific option to be visible
            condition_option_good = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@role='option' and contains(., 'Used - Good')]"))
            )
            condition_option_good.click()
            print("Good condition selected.")
        
        elif condition_choice == 3:
            # Waiting for the specific option to be visible
            condition_option_used = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@role='option' and contains(., 'Used - Fair')]"))
            )
            condition_option_used.click()
            print("Used condition selected.")
        
        else:
            print("Condition not set.")

    except Exception as e:
        print("Error adding condition:", e)

    time.sleep(2)


    # Adding description to the post
    try:
        description_file = r"C:\Users\NEC\Desktop\Facebook Marketing Project\description.txt"
        with open(description_file, "r", encoding='utf-8') as file:
            description = file.read().strip()

        # copying the description using pyperclip
        pyperclip.copy(description)

        description_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'x78zum5')]//textarea"))
        )

        description_box.click()
        description_box.send_keys(Keys.CONTROL, 'v')  # Pasting content using Ctrl+V
        
        #shifting focus of the element
        next_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Price')]/following::input[@type='text'][1]")  # Adjust to actual button XPath
        next_button.click()

        print("Description added successfully.")
    except Exception as e:
        print("Error adding description:", e)

    time.sleep(2)

    try:
        # Prompting user to select a download category
        print("Select a download category:")
        categories = [
            "Tools", "Furniture", "Household", "Garden", "Appliances", "Video Games",
            "Books, Movies & Music", "Bags & Luggage", "Women's clothing & shoes",
            "Men's clothing & shoes", "Jewelry & Accessories", "Health & beauty",
            "Baby & kids", "Toys & Games", "Electronics & computers",
            "Mobile phones", "Miscellaneous"
        ]

        for index, category in enumerate(categories, start=1):
            print(f"{index} = {category}")

        #category_choice = input("Enter the number corresponding to the category: ")
        selected_category = categories[int(category_choice) - 1] if category_choice.isdigit() and 1 <= int(category_choice) <= len(categories) else None

        if selected_category is None:
            raise ValueError("Invalid selection. Please select a valid category.")

        # Selecting download category
        category_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//label[@aria-label='Category' and @role='button']"))
        )
        category_box.click()
        print(selected_category)
        category_option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//span[text()='{selected_category}']"))
        )
        category_option.click()
        print(f"Category selected: {selected_category}")
    except Exception as e:
        print("Error adding category:", e)
    time.sleep(5)



    try:
    # Defining a more stable XPath for the 'More' button
        more_button_xpath = "//div[contains(@class, 'x16n37ib') and contains(@class, 'x1e56ztr')]//i"
    
    # Waiting until the 'More' button is present in the DOM
        more_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, more_button_xpath))
    )
    
    # Creating an ActionChains object
        actions = ActionChains(driver)
    
    # Hovering over the 'More' button to reveal the dropdown menu
        actions.move_to_element(more_button).perform()
        print("Hovered over the 'More' button.")
    
    # Waiting for the dropdown to appear
        time.sleep(3)  # Adjust the sleep time if necessary
    
        # Waiting until the 'More' button is clickable
        more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, more_button_xpath))
        )
        
        # Scroll the 'More' button into view
        driver.execute_script("arguments[0].scrollIntoView();", more_button)
    
        # Click the 'More' button using ActionChains to ensure proper interaction
        actions.move_to_element(more_button).click().perform()
        print("'More' button clicked and dropdown opened.")
    
    except Exception as e:
        print("Error:", e)
    time.sleep(2)
    



    # Adding product tags
    try:
        tags_list = [tag.strip() for tag in product_tags.split(',')]
        print(f"Product tags entered: {tags_list}")

        for tag in tags_list:
            tag_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'x76ihet')]//textarea[contains(@class, 'x1i10hfl') and contains(@class, 'xggy1nq')]"))
            )
            #tag_input.clear()
            driver.execute_script("arguments[0].scrollIntoView();", tag_input)
            tag_input.send_keys(tag)
            tag_input.send_keys(",") 
        print("tags Entered successfully.")
        time.sleep(5)
    
    except Exception as e:
        print("Error: ", e)
    time.sleep(2)


    try:
        # Defining a more stable XPath for the 'More' button
            more_button_xpath = "//div[contains(@class, 'x16n37ib') and contains(@class, 'x1e56ztr')]//i"
        
        # Waiting until the 'More' button is present in the DOM
            more_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, more_button_xpath))
        )
        
        # Creating an ActionChains object
            actions = ActionChains(driver)
        
        # Hovering over the 'More' button to reveal the dropdown menu
            actions.move_to_element(more_button).perform()
            print("Hovered over the 'More' button.")
        
        # Waiting for the dropdown to appear
            time.sleep(3)  # Adjust the sleep time if necessary
        
            # Waiting until the 'More' button is clickable
            more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, more_button_xpath))
            )
            
            # Scroll the 'More' button into view
            driver.execute_script("arguments[0].scrollIntoView();", more_button)
        
            # Click the 'More' button using ActionChains to ensure proper interaction
            actions.move_to_element(more_button).click().perform()
            print("'More' button clicked and dropdown opened.")

            time.sleep(0.5)
        
    except Exception as e:
        print("Error:", e)
    time.sleep(2)




    try:
        with open(r"C:\Users\NEC\Desktop\Facebook Marketing Project\location.txt", "r") as file:
            locations = file.readlines()
        random_location = random.choice(locations).strip()  # Select a random location
        print(f"Random location selected: {random_location}")

        # Set the random location in the Marketplace post
        location_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@aria-label='Location' and @role='combobox']"))
        )
        # Aggressive clear using JS and user simulation
        driver.execute_script("arguments[0].value = '';", location_input)
        time.sleep(1)

        location_input.send_keys("\ue003" * 20)  # Simulate multiple backspaces
        time.sleep(1)

        # Re-focus field and clear again
        driver.execute_script("arguments[0].focus(); arguments[0].select();", location_input)
        location_input.clear()

         # Now input the desired location
        location_input.send_keys(random_location)
        time.sleep(2)


         # Wait for the first suggestion in the dropdown and click it
        first_suggestion = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "(//div[@role='option'])[1]"))
        )
        first_suggestion.click()
        

    except Exception as e:
        print(f'Error adding location: {e}')

    time.sleep(2)



    try:
        # Setting availability to "In Stock"
        availability_option = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//label[@aria-label='Availability']//following-sibling::div//i[@data-visualcompletion='css-img' and contains(@class, 'x1b0d499')]"))
        )
        availability_option.click()
        

        list_in_stock = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[@aria-selected='false']//span[contains(text(), 'In Stock')]"))
        )
        list_in_stock.click()
        print("Availability set to In Stock.")

    except:
        print("no option available")

    time.sleep(2)



    #clicking on the next button
    try:
        element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//div[@role='none']//span[contains(text(), 'Next')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", element)
    #driver.execute_script("arguments[0].click();", element)
        element.click()
        print("Clicked Next button.")
    except:
        print("error clicking next button")


    #clicking on publish button
    try:
        element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Publish')]/ancestor::div[contains(@class, 'x6s0dn4')][1]"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", element)
        #driver.execute_script("arguments[0].click();", element)
        element.click()
        print("Clicked Published button.")
        time.sleep(20)
    except:
        print("error publishing post")

    time.sleep(4)



def open_facebook_marketplace_concurrently():
    credentials_list = get_credentials()
    locations = get_locations()
    
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




# Check if id_filepath and location_file_path are loaded before running
if id_filepath and location_file_path:
    open_facebook_marketplace_concurrently()
else:
    print("Unable to run due to missing id_filepath or location_file_path.")
