from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import os
import getpass
import pandas as pd
import streamlit as st

# Download data from Kinnser-------------------------------------------------------------------------------------------------

def download_data_from_kinnser(branch, agency): 

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    # driver = webdriver.Chrome(service = ChromeService(ChromeDriverManager().install()))
    driver.get("https://kinnser.net/login.cfm")
    username_input = driver.find_element(By.ID, "username")
    username_input.click()
    username_input.send_keys("bpanchal.pwh")
    username_password = driver.find_element(By.ID, "password")
    username_password.click()
    username_password.send_keys("Bittu65@")
    username_login = driver.find_element(By.ID, "login_btn")
    username_login.click()

    username = getpass.getuser()
    download_path = r"C:\Users\{}\Downloads".format(username)

    try:
        alert = driver.switch_to.alert
        print("Alert message:", alert.text)
        alert.accept()
    except Exception as e:
        print("No alert found:", str(e))
    time.sleep(5)

    select_agency = driver.find_element(By.ID, "swapUser")
    select = Select(select_agency)
    branch = branch
    time.sleep(5)
    select.select_by_visible_text(branch)
    time.sleep(5)

    driver.find_element(By.PARTIAL_LINK_TEXT, "Go To").click()
    time.sleep(10)

    driver.find_element(By.PARTIAL_LINK_TEXT, "QA Manager").click()
    time.sleep(10)

    driver.find_element(By.PARTIAL_LINK_TEXT, "Export all data").click()
    time.sleep(15)

    driver.close()

    os.chdir(download_path)
    files = os.listdir(download_path)
    files.sort(key=lambda x: os.path.getmtime(os.path.join(download_path, x)), reverse=True)
    recieved_file = files[0]
    df = pd.read_excel(recieved_file)

    df['Agency'] =  agency

    return df

# Streamlit app-------------------------------------------------------------------------------------------------

if st.button("Click me!"):
    df = download_data_from_kinnser("PathWell Home Health - CT", "CT")
    st.dataframe(df)
