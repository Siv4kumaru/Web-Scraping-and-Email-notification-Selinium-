#https://developer.chrome.com/docs/chromedriver/downloads
#download the chomr web driver
#always run on cmd 
#add the path of chromedriver C:\Program Files (x86)\chromedriver.exe
#if not working put path variable using service import inside driver
from selenium import webdriver
from selenium.webdriver.common.by import By
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
driver.execute_script("window.open('https://incometaxindia.gov.in/Pages/communications/notifications.aspx', '_blank');")
all_tabs = driver.window_handles

file_name="data.csv"

  # try is for all dynamic 
def get_data():
    driver.switch_to.window(all_tabs[0])
    pageOne=[]
    parent_element1 = driver.find_element(By.ID, "dvMainContents")
    searchResult=parent_element1.find_elements(By.XPATH, "./div[@class='search_result']")
    for i in searchResult:
      linkArray1=i.find_element(By.TAG_NAME, "a").get_attribute("onclick").split("'")[1]
      link=linkArray1.split(".pdf&")[0]+".pdf"
      arr=i.text.split("\n")[:2]
      arr.append(link)
      pageOne.append(arr)
    driver.close()
    

    # dummy=["d","u","mmy"]
    # pageOne.append(dummy)
    db(pageOne,"circulars")
    driver.switch_to.window(all_tabs[1])
    pagetwo_Noti=[]

    parent_element2 = driver.find_element(By.ID, "dvMainContents")
    pagetwo=parent_element2.find_elements(By.XPATH, "./div[@class='search_result']")
    for i in pagetwo:
      
      linkelement=i.find_element(By.TAG_NAME, "a")

      linkArray=linkelement.get_attribute("onclick").split("'")[1]
      
      link=linkArray.split(".pdf&")[0]+".pdf"
      arr=i.text.split("\n")[:2]
      arr.append(link)
      pagetwo_Noti.append(arr)
    
    db(pagetwo_Noti,"notifications")
    driver.quit()
    

  
def db(page,type):
    try:
        for i in page:
            if session.query(Table).filter(Table.Title == i[0]).first() is None:
                new_entry = Table(
                    Title=i[0],
                    Datetime=i[1],
                    Link=i[2] ,
                    Email_Sent=False,
                    Type=type
                )
                print("New entry Added to the database")
                session.add(new_entry)
            else:
                print("Already in the database")
        session.commit()  # Commit all changes after the loop
    except Exception as e:
         session.rollback()  # Rollback in case of error
         print(f"An error occurred: {e}")

def condition():
    email_list = []
    for i in session.query(Table).filter(Table.Email_Sent == False).all():
        i.Email_Sent = True
        email_list.append([i.Title,i.Datetime,i.Link,i.Type])
        session.commit()
        print("email sending")
    
    if len(email_list)>0:
        mailu(email_list)
        print("email sent")
        return
    else:
        print("No email to send")
        return




session.close()  # Ensure the session is closed
get_data()
condition()

  



#driver.close() for tab



