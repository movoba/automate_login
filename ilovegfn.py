from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import os
import schedule

import time


heute = datetime.now().date()
daten = []

with open('daten.csv') as csvdatei:
    datum = csv.reader(csvdatei)
    for row in datum:
        datumObj = datetime.strptime(row[0], '%Y-%m-%d').date()
        daten.append(datumObj)
        



username = os.environ.get("username")
password = os.environ.get("password")

chrome_driver_path = "path_to_chrome_driver"

service = Service(executable_path=chrome_driver_path)

options = webdriver.ChromeOptions()
#Argument um die Chrome Sandbox zu deaktivieren. muss um zu laufen
options.add_argument('--no-sandbox')  
#damit Chrome nicht geschlossen wird     
options.add_experimental_option("detach",True)
options.add_experimental_option('excludeSwitches', ['enable-logging'])


driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(3)
driver.get("https://lernplattform.gfn.de/login/index.php")

def automate_login(username, password):
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)               
    log_in_button = driver.find_element(By.ID, "loginbtn")
    log_in_button.click()
    standort = driver.find_element(By.ID, "flexRadioDefault2")
    standort.click()
    anmelden = driver.find_element(By.CSS_SELECTOR, "input[value='starten']")
    anmelden.click()
    ausloggen()


def automate_logout(username, password):
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)               
    log_in_button = driver.find_element(By.ID, "loginbtn")
    log_in_button.click()
    abmelden = driver.find_element(By.CSS_SELECTOR, "a[href='?stoppen=1']")
    abmelden.click()
    ausloggen()

def ausloggen():
    dropdown = driver.find_element(By.ID, "user-menu-toggle")
    dropdown.click()
    item_select = driver.find_element(By.LINK_TEXT, "Logout")
    item_select.click()


if heute in daten:
        schedule.every().day.at("08:21").do(automate_login, username, password)
        schedule.every().day.at("16:31").do(automate_logout, username, password)


    
while True:
    schedule.run_pending()
    time.sleep(1)