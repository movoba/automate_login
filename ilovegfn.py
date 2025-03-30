#! /usr/bin/python3
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoAlertPresentException
import os
import logging
import time



class WebNav:
    def __init__(self, load_zugangsdaten):
        self.zugangsdaten = load_zugangsdaten
        self.path_to_webdriver = os.environ.get("path_to driver")
        driver = self.driver_starten()
        self.automate_login(driver)
        self.automate_logout(driver)
        self.ausloggen(driver)

    def driver_starten(self):
        try:
            service = Service(self.path_to_webdriver)
            options = webdriver.ChromeOptions()
            options.add_argument("--no-sandbox")
            options.add_experimental_option("detach", True)
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            driver = webdriver.Chrome(service=service, options=options)
            driver.implicitly_wait(4)
            driver.get("https://lernplattform.gfn.de/login/index.php")
            logging.info("Webdriver laeuft")
            return driver
        except Exception as e:
            logging.error(f"Fehler beim Laden des drivers: {e}")

    def automate_login(self, driver):
        username = self.zugangsdaten['username']
        passwort = self.zugangsdaten['passwort']
        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(passwort)
        log_in_button = driver.find_element(By.ID, "loginbtn")
        log_in_button.click()
        try:
            alert = Alert(driver)
            alert.accept()
        except NoAlertPresentException:
            pass
        try:
            aside = driver.find_element(
                By.CSS_SELECTOR, "button[title='Blockleiste öffnen']"
            )
            aside.click()
        except:
            print("Kein aside vorhanden")
        standort = driver.find_element(
            By.CSS_SELECTOR, "input[name='homeo'][value='2']"
        )
        standort.click()
        anmelden = driver.find_element(By.CLASS_NAME, "btn-primary")
        anmelden.click()
        self.ausloggen(driver)
        back_to_log_in = driver.find_element(By.CLASS_NAME, "login")
        back_to_log_in.click()
        driver.find_element(By.ID, "username").clear()

    def automate_logout(self, driver):
        username = self.zugangsdaten['username']
        passwort = self.zugangsdaten['passwort']
        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(passwort)
        log_in_button = driver.find_element(By.ID, "loginbtn")
        log_in_button.click()
        try:
            aside = driver.find_element(
                By.CSS_SELECTOR, "button[title='Blockleiste öffnen']"
            )
            aside.click()
        except:
            print("Kein aside vorhanden")
        time.sleep(3)
        abmelden = driver.find_element(By.CLASS_NAME, "btn-primary")
        abmelden.click()
        self.ausloggen(driver)
        back_to_log_in = driver.find_element(By.CLASS_NAME, "login")
        back_to_log_in.click()
        driver.find_element(By.ID, "username").clear()

    def ausloggen(self, driver):
        dropdown = driver.find_element(By.ID, "user-menu-toggle")
        dropdown.click()
        item_select = driver.find_element(By.LINK_TEXT, "Logout")
        item_select.click()
