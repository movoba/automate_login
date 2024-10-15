from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
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

chrome_driver_path = "PATH"

service = Service(executable_path=chrome_driver_path)

options = webdriver.ChromeOptions()
#Argument um die Chrome Sandbox zu deaktivieren. muss um zu laufen
options.add_argument('--no-sandbox') 

#nur wenn stabil läuuft. fenster öffnet sich dann nicht mehr
#options.add_argument("--headless")


#damit Chrome nicht geschlossen wird     
options.add_experimental_option("detach",True)
#unnötiges logging ausschließen
options.add_experimental_option('excludeSwitches', ['enable-logging'])


driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(3)
driver.get("https://lernplattform.gfn.de/login/index.php")
alert = Alert(driver)

def automate_login(username, password):
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)        
    log_in_button = driver.find_element(By.ID, "loginbtn")
    log_in_button.click()
    alert.accept()
    try:
        aside = driver.find_element(By.CSS_SELECTOR, "button[title='Blockleiste öffnen']")
        aside.click()
    except:
        print("Kein aside vorhanden")
    standort = driver.find_element(By.CSS_SELECTOR, "input[value='2']")  #(By.ID, "flexRadioDefault2")
    standort.click()
    anmelden = driver.find_element(By.CLASS_NAME, "btn-primary")
    anmelden.click()
    ausloggen()
    back_to_log_in = driver.find_element(By.CLASS_NAME, "login")
    back_to_log_in.click()



def automate_logout(username, password):
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)               
    log_in_button = driver.find_element(By.ID, "loginbtn")
    log_in_button.click()
    try:
        aside = driver.find_element(By.CSS_SELECTOR, "button[title='Blockleiste öffnen']")
        aside.click()
    except:
        print("Kein aside vorhanden")
    time.sleep(3)
    abmelden = driver.find_element(By.CLASS_NAME, "btn-primary")
    abmelden.click()
    ausloggen()
    back_to_log_in =driver.find_element(By.CLASS_NAME, "login")
    back_to_log_in.click()



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