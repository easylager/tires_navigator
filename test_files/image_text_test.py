from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup
import requests
from PIL import Image
from datetime import datetime

class Bot:
    def __init__(self):
        self.driver = webdriver.Chrome(
            r'/drivers/chromedriver.exe'

        )
        self.navigate()

    def take_screenshot(self):
        self.driver.save_screenshot('kufar_phone_number_screenshot.png')

    def crop(self, location, size):
        image = Image.open('kufar_phone_number_screenshot.png')
        x = location['x']
        y = location['y']
        width = size['width']
        height = size['height']

        image.crop((x, y, x+width, y+height)).save('telephone.png')


    def navigate(self):
        start = datetime.now()
        self.driver.get('https://auto.kufar.by/vi/139509611')

        button = self.driver.find_element(By.XPATH, "//button[@class='kf-Uap-7e49f kf-Uub-da81f kf-UuQ-f630e']")

        button.click()
        sleep(3)
        self.take_screenshot()
        end = datetime.now()
        lenght = end - start
        print(lenght)
        phone_number = self.driver.find_element(By.XPATH, '//a[@class="kf-qrLj-cf8c7"]')
        location = phone_number.location
        size = phone_number.size
        print(location, size)
        self.crop(location, size)




def main():
    bot = Bot()


if __name__ == '__main__':
     main()
