#! /usr/bin/python3
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoAlertPresentException
import csv
import os
import schedule
import logging
import time

logging.basicConfig(filename='error.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

heute = datetime.now().date()
daten = []

with open('daten.csv',  encoding='utf-8') as csvdatei:
    datum = csv.reader(csvdatei)
    for row in datum:
        datumObj = datetime.strptime(row[0], '%Y-%m-%d').date()
        daten.append(datumObj)
        

username = os.environ.get("username")
password = os.environ.get("password")
path_to_webdriver = os.environ.get("path_to driver")

if not username or not password:
    logging.error("Umgebungsvariablen fuer Benutzername oder Passwort fehlen.")
    raise ValueError("Benutzername oder Passwort sind nicht gesetzt.")

def driver_starten():
    try:
        service = Service(path_to_webdriver)
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox') 
        options.add_experimental_option("detach",True)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(4)
        driver.get("https://lernplattform.gfn.de/login/index.php")
        logging.info("Webdriver laeuft")
        return driver
    except Exception as e:
        logging.error(f"Fehler beim Laden des drivers: {e}")

driver = driver_starten()

def automate_login(username, password, driver):
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)        
    log_in_button = driver.find_element(By.ID, "loginbtn")
    log_in_button.click()
    try:
        alert = Alert(driver)
        alert.accept()
    except NoAlertPresentException:
        pass
    try:
        aside = driver.find_element(By.CSS_SELECTOR, "button[title='Blockleiste öffnen']")
        aside.click()
    except:
        print("Kein aside vorhanden")
    standort = driver.find_element(By.CSS_SELECTOR, "input[name='homeo'][value='2']")
    standort.click()
    anmelden = driver.find_element(By.CLASS_NAME, "btn-primary")
    anmelden.click()
    ausloggen(driver)
    back_to_log_in = driver.find_element(By.CLASS_NAME, "login")
    back_to_log_in.click()
    driver.find_element(By.ID, "username").clear()



def automate_logout(username, password, driver):
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
    ausloggen(driver)
    back_to_log_in =driver.find_element(By.CLASS_NAME, "login")
    back_to_log_in.click()
    driver.find_element(By.ID, "username").clear()


def ausloggen(driver):
    dropdown = driver.find_element(By.ID, "user-menu-toggle")
    dropdown.click()
    item_select = driver.find_element(By.LINK_TEXT, "Logout")
    item_select.click()


if heute in daten:
        schedule.every().day.at("08:21").do(automate_login, username, password, driver)
        schedule.every().day.at("16:31").do(automate_logout, username, password, driver)
        
if __name__ == "__main__":
    while True:
        schedule.run_pending()
        #logging.info("Warte auf naechste geplante Aufgabe...")
        time.sleep(1)
