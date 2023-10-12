#Below we are importing the required packages for this project
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,NoSuchElementException,WebDriverException
from bs4 import BeautifulSoup
import time
import pandas as pd
url = "https://fcainfoweb.nic.in/reports/report_menu_web.aspx" #URL of the given website for Web Scraping

for m in range(26,36): #Since from August 1 to September 30, a total of 61 days are there, we are running the loop for 61 times
    try:
        date = "//2023"#The specified date for which the data is to be extracted
        #Below we are formatting the date string for the Web Scraping
        if(m<=31):
            if(m<10):
                date = "0"+str(m)+"/08/2023"
            else:
                date =  str(m)+"/08/2023"
        else:
            if((m-31)<10):
                date = "0"+str(m-31)+"/09/2023"
            else:
                date =  str(m-31)+"/09/2023"
        
        Report_type_id = "ctl00_MainContent_Ddl_Rpt_type" #The Id of the report type selection tag on the webpage
        browser = webdriver.Firefox()# defining the browser, in this case Firefox
        browser.get(url)#Initializing a browser instance
        Report_type_sel = browser.find_element(By.ID, Report_type_id)#Finding the report selection element on the webpage by its id
        select = Select(Report_type_sel)#Converting it to a select type item
        select.select_by_value("Retail")#Selecting value of the select tag 
        price_data_input_tag_id = "ctl00_MainContent_Rbl_Rpt_type_0" #The radio button id on the webpage
        price_data_input_tag = browser.find_element(By.ID, price_data_input_tag_id) 
        price_data_input_tag.click()#After finding the element, clicking it
        Daily_prices_tag_id = "ctl00_MainContent_Ddl_Rpt_Option0"
        Daily_prices_tag = browser.find_element(By.ID, Daily_prices_tag_id)
        select2 = Select(Daily_prices_tag)#Selecting the Daily prices from the next selection tag on the webpage
        select2.select_by_value("Daily Prices")
        Date_select_tag_id = "ctl00_MainContent_Txt_FrmDate"#Selecting the Date element(The one we are using to set the dates for the data)
        Date_select_tag = browser.find_element(By.ID, Date_select_tag_id)
        Date_select_tag.send_keys(date)#Setting the date by sending a key value to the element
        Get_Data_button_ID = "ctl00_MainContent_btn_getdata1"
        Get_Data_button = browser.find_element(By.ID, Get_Data_button_ID)
        Get_Data_button.click()#Clicking on the Get Data Button

        # Wait for the page to load (you may need to modify this based on the specific page load times
        myElem = WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.ID, 'gv0')))
        new_url = browser.current_url#Since the web page is opening a new link after clicking on Get Data, grabbing the new link
        response = requests.get(new_url)
        new_page = response.content#Referencing the new page of the element
        myElem = WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'MyCssClass')))

        # Find the div element with the class "MyCssClass"
        data_div = browser.find_element(By.CLASS_NAME, "MyCssClass")

        # Extract the data from the div using BeautifulSoup
        data_soup = BeautifulSoup(data_div.get_attribute("outerHTML"), "html.parser")

        data_table = data_soup.find("table")

        # Extract data from the table as needed
        rows = data_table.find_all("tr")
        header=[]
        for i in rows[0].find_all('th'):
            header.append(i.text.strip())
        data = [[j.text.strip() for j in row.find_all('td')]for row in rows[5:]]


        #Below is the algorithm that sets the name of the CSV files based on date and groups them into separate folders for the months of August and September
        AG_folder_path = "C:/Users/HRITHIMAN GUHA/Desktop/IITK/August_CSV"
        SP_folder_path = "C:/Users/HRITHIMAN GUHA/Desktop/IITK/September_CSV"
        file_name = ""
        if(m<=31):
            #This avoids lexicographical arrangement of the data in the final CSV. Lexicographical arrangement means, it'll be arranged like 1,10,11,12.. Adding a 0 for single digit elements prevents this from happening
            if(m<10):
                file_name = "retail_prices_2023-08-0"+str(m)+".csv"
                df = pd.DataFrame(data,columns=header)                      
                df.to_csv(f"{AG_folder_path}/{file_name}", index=False)
            else:

                file_name = "retail_prices_2023-08-"+str(m)+".csv"
                df = pd.DataFrame(data,columns=header)                      
                df.to_csv(f"{AG_folder_path}/{file_name}", index=False)
        else:
            if((m-31)<10):
                file_name = "retail_prices_2023-09-0"+str(m-31)+".csv"
                df = pd.DataFrame(data,columns=header)                      
                df.to_csv(f"{SP_folder_path}/{file_name}", index=False)
            else:

                file_name = "retail_prices_2023-09-"+str(m-31)+".csv"
                df = pd.DataFrame(data,columns=header)                      
                df.to_csv(f"{SP_folder_path}/{file_name}", index=False)
            
        browser.quit() 
    except (TimeoutException, NoSuchElementException, WebDriverException) as e:
        with open("error.log", "w") as error_file:
            error_file.write("An error occured: "+str(e))
    

import os

# Create an empty list to store DataFrames
dataframes = []

# List of folder names containing CSV files
folders = ["August_CSV", "September_CSV"]

for folder in folders:
    folder_path = os.path.join(os.getcwd(), folder)  # Assumes the folders are in the current working directory

    # Loop through each CSV file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            def extract_date(file): #Function to determine the date from the filename
                return file[14:24]
            # Read the CSV file into a DataFrame
            data = pd.read_csv(file_path)

            
            new_row = pd.DataFrame({'States/UTs': [extract_date(str(filename))], 'Rice': [None]})  # Adjust column names as needed

            # Concatenate the new row with the existing DataFrame
            data = pd.concat([new_row,data], ignore_index=True)

            # Append the modified DataFrame to the list
            dataframes.append(data)

# Concatenate the list of DataFrames into one DataFrame
combined_data = pd.concat(dataframes, ignore_index=True)


output_file = 'retail_prices_data_aug_to_sep.csv' 

combined_data.to_csv(output_file, index=False)#Creating the Final CSV file
