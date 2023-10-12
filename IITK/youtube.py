from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
# Set up the Selenium webdriver (you can use other browsers like Firefox or Edge)
driver = webdriver.Firefox()

# Navigate to the YouTube website
driver.get("https://www.youtube.com")

# Use an explicit wait to wait for the search input element to be clickable
wait = WebDriverWait(driver, 10)
search_input = wait.until(EC.element_to_be_clickable((By.NAME, "search_query")))

# Clear any existing text in the search input
search_input.clear()

# Enter your search query
search_query = "your search query here"
search_input.send_keys(search_query)

# Simulate hitting the Enter key to perform the search
search_input.send_keys(Keys.RETURN)

# Wait for a few seconds to see the results
time.sleep(5)

# Close the browser
driver.quit()
