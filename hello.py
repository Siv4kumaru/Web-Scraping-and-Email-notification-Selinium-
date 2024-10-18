#https://developer.chrome.com/docs/chromedriver/downloads
#download the chomr web driver
#add the path of chromedriver C:\Program Files (x86)\chromedriver.exe
#if not working put path variable using service import inside driver
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import csv
from bs4 import BeautifulSoup 
import pandas as pd
from autoMail import mailu
import time


driver = webdriver.Chrome()

driver.get("https://incometaxindia.gov.in/Pages/communications/circulars.aspx")

  # try is for all dynamic 
titles=[]
def get_data():
    try:
        time.sleep(10)
        newsearch = driver.find_element(By.ID, "ctl00_SPWebPartManager1_g_5dfb7f33_6e2c_4d3e_b244_c2874a376703_txtNumber")
        newsearch.send_keys("1")
        newsearch.send_keys(Keys.RETURN)
        time.sleep(10)
        newTag=driver.find_elements(By.TAG_NAME, "sup")
        newTag=driver.find_element(By.TAG_NAME, "sup")
        clickable=driver.find_element(By.CLASS_NAME, "NotificationNumber")
        clickable.click()
        
        
        new=[i.text for i in newTag if(i.text)]
        for i in newTag:
          if i.text:
            sibling_element = driver.execute_script("return arguments[0].previousElementSibling.innerHTML;", i)
            print(sibling_element)
            soup=BeautifulSoup(sibling_element, 'html.parser')
            notification_number = soup.find('span', class_='NotificationNumber').text.strip()
            guidance_note = soup.get_text(strip=True).split(notification_number)[1].split(soup.find('span', class_='publishDate').text.strip())[0].strip()
            publish_date = soup.find('span', class_='publishDate').text.strip()

            
            # Print the resultscls
            json={"Notification Number:": notification_number,
            "Guidance Note:": guidance_note,
            "Publish Date:": publish_date}
            
            titles.append(json)
        
        print(new)
        emptySearch=driver.find_element(By.CLASS_NAME, "act_search_header")
        lastUpdated=driver.find_element(By.CLASS_NAME, "lastupdated")
        record=emptySearch.text.split(" ")[0]
        date_string=lastUpdated.text.split(": ")[1]
        datetime_obj = datetime.strptime(date_string, "%d %B %Y").date()
        today=datetime.now().date()
        print(f"Date of Checking:{today}")
        print(f"Record:{record}")
        print(f"Last Updated:{datetime_obj}")
        #toCSV(today,record,datetime_obj)
    except:
        print("error finding elements")
        return 


def toCSV(today,number,update):
    print("csv creation...")
    file_name="data.csv"
    file_exists = os.path.isfile(file_name)
    try:   
      with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)

        # If the file doesn't exist, write the header first
        if not file_exists:
            writer.writerow(['ID', "Date of checking", "Record no", "Last Update","Check"])  # Example headers
            print("data.csv is created...")
      
        writer.writerow([len(open(file_name).readlines()), today, number, update,False])
      print("CSV creation Success")
      condition() 
    except Exception as e:
      print(f"failed to create CSV:{e}")

def condition():
    try:
      df = pd.read_csv("data.csv")
      print(df)
      # Convert "Date of checking" and "Last Update" columns to datetime format
      df['Date of checking'] = pd.to_datetime(df['Date of checking'])
      df['Last Update'] = pd.to_datetime(df['Last Update'])
      
      # Iterate through the rows and check if "Date of checking" is greater than "Last Update"

      if(len(df)>1):
        last_row=df.iloc[-1]
        last_but2=df.iloc[-2]
        if last_row['Date of checking'] >= last_row['Last Update']:
          if not (last_row['Check']) and last_row['Last Update'] != last_but2['Last Update']:
            df.loc[df.index[-1], 'Check'] = True
            df.to_csv("data.csv", index=False)
            print("email sending")
            #email here
            mailu(titles)
            return
          if last_row['Last Update'] == last_but2['Last Update'] and (last_but2['Check']):
            df.loc[df.index[-1], 'Check'] = True
            df.to_csv("data.csv", index=False)
            print("alredy sent Email")
            return
      elif(len(df)==1):
        print(df)
        row=df.iloc[0]
        if row['Date of checking'] >= row['Last Update']:
          if not (row['Check']):
            df.loc[df.index[0], 'Check'] = True
            df.to_csv("data.csv", index=False)
            print("<1st entry> email sending")
            #email here
            mailu(titles)
            return
      else:
          print("No data found.")
    
    except FileNotFoundError:
        print("Error: CSV file not found.")
        
    except Exception as e:
       print(f"conditional Error {e}")


    
get_data()
  




#driver.close() for tab
driver.quit()


