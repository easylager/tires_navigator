from selenium import webdriver
import requests
from time import sleep
from selenium.webdriver.common.by import By

def get_number(url):

    driver = webdriver.Chrome()
    driver.get(url=url)
    button = driver.find_element(By.XPATH, "//button[@class='kf-Uap-7e49f kf-Uub-da81f kf-UuQ-f630e']")
    button.click()
    sleep(2)
    number = driver.find_element(By.XPATH, '//a[@class="kf-qrLj-cf8c7"]').text.strip()
    return number

get_number()