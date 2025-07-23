import os
import pickle
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time


# Constants:
COOKIES_FILE = "res/steam_cookies.pkl"


def _save_cookies(cookies, filename):
    with open(filename, "wb") as f:
        pickle.dump(cookies, f)


def _load_cookies(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)


def _cookies_valid(session):
    # Try to access a page that requires login
    resp = session.get("https://steamcommunity.com/")
    return False # "Login" not in resp.text


def get_session_with_cookies(username, password):
    session = requests.Session()

    if os.path.exists(COOKIES_FILE):
        cookies = _load_cookies(COOKIES_FILE)

        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])

        if _cookies_valid(session):
            print("Using saved cookies.")
            return session
        
        else:
            print("Saved cookies invalid, logging in again.")

    # Login with Selenium if no valid cookies
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(800, 800)
    driver.get("https://steamcommunity.com/login/home/")
    time.sleep(2)
    driver.find_element(By.XPATH, '//input[@type="text"]').send_keys(username)
    driver.find_element(By.XPATH, '//input[@type="password"]').send_keys(f'{password}\n')
    time.sleep(15)  # Wait for manual 2FA if needed
    cookies = driver.get_cookies()
    _save_cookies(cookies, COOKIES_FILE)

    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])
    
    driver.quit()

    return session
