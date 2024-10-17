#https://developer.chrome.com/docs/chromedriver/downloads
#download the chomr web driver
#add the path of chromedriver C:\Program Files (x86)\chromedriver.exe
#if not working put path variable using service import inside driver
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import csv
import pandas as pd


driver = webdriver.Chrome()

driver.get("https://incometaxindia.gov.in/Pages/communications/circulars.aspx")

  # try is for all dynamic 
def get_data():
    try:
        newTag=driver.find_elements(By.TAG_NAME, "sup")
        new=[i.text for i in newTag if(i.text)]
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
        toCSV(today,record,datetime_obj)
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


