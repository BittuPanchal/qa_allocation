import streamlit as st
import os
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time
import getpass
import pandas as pd

@st.cache_resource
def get_driver():
    import os
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager

    # Force specific ChromeDriver version by setting env variable
    os.environ['WDM_CHROMEDRIVER'] = '120.0.6099.224'

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.binary_location = "/usr/bin/chromium"

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    return driver


def download_data_from_kinnser(driver, branch, agency): 

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

# Streamlit UI
if st.button("Click me!"):
    driver = get_driver()
    df = download_data_from_kinnser(driver, "PathWell Home Health - CT", "CT")
    st.dataframe(df)
