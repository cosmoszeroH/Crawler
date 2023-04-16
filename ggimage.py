import os
import time
import requests
import urllib.request

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.microsoft import EdgeChromiumDriverManager


def create_project_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


name = input("Image title: ")
create_project_dir('image/' + name)

driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
driver.get("https://www.google.com/imghp?hl=en")  # Link gg images
elem = driver.find_element(By.CLASS_NAME, "gLFyf")
elem.send_keys(name)
elem.send_keys(Keys.ENTER)

SCROLL_PAUSE_TIME = 1

# Lay toan bo hinh anh tim duoc
last_height = driver.execute_script("return document.body.scrollHeight")
while True:

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Doi load them anh
    time.sleep(SCROLL_PAUSE_TIME)

    new_height = driver.execute_script("return document.body.scrollHeight")
    # Test xem con anh de load ko
    if new_height == last_height:
        try:
            driver.find_element(By.CSS_SELECTOR, ".mye4qd").click()
        except:
            break
    last_height = new_height

images = driver.find_elements(By.CSS_SELECTOR, ".rg_i.Q4LuWd")
count = 1
for image in images:
    try:
        image.click()
        time.sleep(2)

        imgUrl = image.get_attribute("src")

        urllib.request.urlretrieve(imgUrl, 'image/' + str(name) + "/" + str(name) + "_" + str(count).zfill(3) + ".jpg")
        count = count + 1
    except:
        pass

driver.close()
