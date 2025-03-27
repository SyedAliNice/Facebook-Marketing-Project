
# Facebook Marketplace Automation 
![image alt]()

This tool automates the process of creating and managing listings on Facebook Marketplace using Selenium WebDriver.
#   Features
1.  Multi-account support: Logs into multiple Facebook accounts from credentials file
2.  Location targeting: Posts listings in different geographic locations
3.  Campaign management: Saves and loads campaign configurations
4.  Concurrent posting: Posts listings simultaneously across multiple accounts
5.  Dynamic content: Randomizes titles, prices, and locations for each post
6.  Media uploads: Automatically uploads product images
#   File Structure
1.  credentials.txt: Contains Facebook account credentials (username/password pairs)
2.  location.txt: List of target locations for Marketplace posts
3.  description.txt: Product description template
4.  Transform Your Living Space with Ou.txt: List of product title variations
5.  sofa_campain.csv: Stores campaign configurations
6.  main.py: Main automation script
7.  remove_duplicates.py: Utility script for account management
8.  sample.py: Example script
#   Setup Instructions
1.  Install required Python packages: pip install selenium webdriver-manager pandas pyperclip
2.  Prepare your files: Add Facebook account credentials to credentials.txt in format: username=your_username and  password=your_password
3.  Add target locations to location.txt (one per line)
4.  Add product description to description.txt
5.  Add product title variations to Transform Your Living Space with Ou.txt
#   Configure campaign settings in main.py:
1.  Set paths to your files
2.  Define price ranges and product conditions
3.  Select product categories
#   Usage
Run the main script:
python main.py

You will be prompted to:
1.  Choose between creating a new campaign or loading an existing one
2.  Enter campaign details (if creating new)
3.  Specify number of concurrent tabs to open
#   Campaign Configuration
The tool supports saving and loading campaign configurations including:

1.  Campaign name
2.  Title file path
3.  Price range (min/max)
4.  Product condition
5.  Description file
6.  Product tags
7.  Category selection
8.  Credentials file path
9.  Locations file path
10. Images folder path
#   Notes
1.  The script includes error handling for common Facebook Marketplace interactions
2.  Uses headless Chrome browser by default (can be disabled)
3.  Includes delays between actions to mimic human behavior
4.  Randomizes elements (titles, prices, locations) to avoid detection



