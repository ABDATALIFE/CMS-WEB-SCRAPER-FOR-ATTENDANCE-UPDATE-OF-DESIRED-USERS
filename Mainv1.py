import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
#import schedule
import hashlib
import time
from twilio.rest import Client

def get_employee_status_dynamic(url, username, password):
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    
    # Log in to the website
    driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$txtUserName').send_keys(username)
    driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$txtPassword').send_keys(password)
    driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$Button1').click()
    
    # Wait for login to complete and dashboard to load
    time.sleep(5)  # Adjust sleep time as needed
    
    # Navigate to 'Current Attendance Report'
    driver.find_element(By.LINK_TEXT, 'Current Attendance Report').click()
    
    # Wait for the attendance report to load
    time.sleep(5)  # Adjust sleep time as needed
    
    # Extract the table data
    attendance_data = []
    table = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_GrdCurrentReport')
    rows = table.find_elements(By.TAG_NAME, 'tr')
    
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, 'td')
        if cols:
            employee_name = cols[0].text
            time_in = cols[1].text
            time_out = cols[2].text
            attendance_data.append({
                'Employee Name': employee_name,
                'Time In': time_in,
                'Time Out': time_out
            })
    
    driver.quit()
    return attendance_data



def send_whatsapp_message(message, to_whatsapp_number):
    account_sid = '[SSID]'
    auth_token = '[AUTH]'
    client = Client(account_sid, auth_token)
    message_hash = hashlib.md5(message.encode()).hexdigest()
    
    client.messages.create(
        body=message,
        from_='whatsapp:[TWILIO NUMBER]',
        to=f'whatsapp:[YOUR NUMBER]'
    )





def check_for_updates():
    # URL, username, and password for the CMS
    url = 'https://zabcms.szabist.edu.pk/'
    username = '[USERNAME]'
    password = '[PASSWORD]'
    
    # Get employee status from the "Current Attendance Report"
    attendance_data = get_employee_status_dynamic(url, username, password)

    # List of employee names to monitor
    desired_contacts = [DESIRED PERSONS]

    # Check for specific employee status and send notifications if needed
    for record in attendance_data:
        if record['Employee Name'] in desired_contacts:
            message = f"Employee {record['Employee Name']} has signed in at {record['Time In']} or signed out at {record['Time Out']}"
            send_whatsapp_message(message, '[YOUR WHATSAPP NUMBER]')
            
    
    
    
            
    
    





if __name__ == "__main__":
    check_for_updates()