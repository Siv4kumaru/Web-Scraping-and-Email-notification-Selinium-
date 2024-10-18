#https://developer.chrome.com/docs/chromedriver/downloads
#download the chomr web driver
#add the path of chromedriver C:\Program Files (x86)\chromedriver.exe
#if not working put path variable using service import inside driver
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from sqlalchemy import create_engine
from autoMail import mailu
from model import Table
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'sqlite:///example.db'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
driver = webdriver.Chrome()
session = Session()  # Assuming Session is already defined and configured
driver.get("https://incometaxindia.gov.in/Pages/communications/circulars.aspx")
file_name="data.csv"

  # try is for all dynamic 
def get_data():
    pageOne=[]
    searchResult=driver.find_elements(By.CLASS_NAME, "search_result")
    for i in searchResult:
      linkArray1=i.find_element(By.TAG_NAME, "a").get_attribute("onclick").split("'")[1]
      link=linkArray1.split(".pdf&")[0]+".pdf"
      arr=i.text.split("\n")[:2]
      arr.append(link)
      pageOne.append(arr)
    # dummy=["d","u","mmy"]
    # pageOne.append(dummy)
    db(pageOne)

  
def db(pageOne):
    try:
        for i in pageOne:
            if session.query(Table).filter(Table.Title == i[0]).first() is None:
                new_entry = Table(
                    Title=i[0],
                    Datetime=i[1],
                    Link=i[2],
                    Email_Sent=False
                )
                print("New entry Added to the database")
                session.add(new_entry)
            else:
                print("Already in the database")
        condition()
        session.commit()  # Commit all changes after the loop
    except Exception as e:
        session.rollback()  # Rollback in case of error
        print(f"An error occurred: {e}")

def condition():
    email_list = []
    for i in session.query(Table).filter(Table.Email_Sent == False).all():
        i.Email_Sent = True
        email_list.append([i.Title,i.Datetime,i.Link])
        session.commit()
        print("email sent")
    if len(email_list)>0:
        mailu(email_list)



session.close()  # Ensure the session is closed
get_data()

  



#driver.close() for tab
driver.quit()


