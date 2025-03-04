
## Web Scraping and Email Notification with Selenium

Site Scraped:

  ![image](https://github.com/user-attachments/assets/45434377-0e2b-4faf-bc90-3189959aa770)

Email Received:

  ![image](https://github.com/user-attachments/assets/8395469e-e2f0-4c52-a75a-c3204fbc53b2)


This project scrapes data from a https://incometaxindia.gov.in/Pages/communications/notifications.aspx daily, organizes it, and sends email notifications to specified recipients if new entries are detected. It uses Selenium for web scraping and an SMTP server for email notifications.
Requirements

    Python 3.8 or above
    Note: The original requirement mentioned "Python 8 or above," which is likely a typo, as Python is currently at version 3.x. This project assumes Python 3.8 or higher.

## Installation



  ### Clone the repository:
      git clone https://github.com/Siv4kumaru/Web-Scraping-and-Email-notification-Selinium-
      cd Web-Scraping-and-Email-notification-Selinium-
      pip install -r requirements.txt 

Configuration

To configure email notifications, create a .env file in the project root directory with the following content:
text 

      EMAIL_SENDER=sender@gmail.com
      EMAIL_PASSWORD=<google app password>
      EMAIL_RECEIVER=receiver1@gmail.com,receiver2@gmail.com
      Environment Variables Explained:

EMAIL_SENDER: Your Gmail address used to send the notifications.
EMAIL_PASSWORD: Your Google App Password (not your regular Gmail password). Generate one at Google App Passwords.
EMAIL_RECEIVER: A comma-separated list of email addresses that will receive the notifications.

Replace the placeholders (sender@gmail.com, <google app password>, receiver1@gmail.com,receiver2@gmail.com) with your actual credentials.
Usage

To run the application, follow these steps:

  Open a terminal and navigate to the project directory (if not already there).
  Execute the following command:
     python app.py

How It Works

    The script uses Selenium to scrape data from a specified website every day.
    It stores the scraped data in an organized manner.
    On subsequent runs, it compares the new data with the previous data. If new entries are found, it dynamically sends an email notification to the recipients listed in EMAIL_RECEIVER.
