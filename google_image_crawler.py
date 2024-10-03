# Used to crawl images from Google Scholar website

import urllib.request

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

from threading import Thread

from bs4 import BeautifulSoup

from time import sleep

from utils import create_directory


SITE = r"https://www.google.com/imghp?hl=en"
SCROLL_NUM = 5


# Using thread to boost the crawl speed
class Image(Thread):
    def __init__(self, image, count, name):
        super().__init__()
        self.image = image
        self.count = count
        self.name = name

    def run(self):
        try:
            # Get the image's source
            imgUrl = self.image.get_attribute("src")

            urllib.request.urlretrieve(imgUrl, str(self.name) + "/" + str(self.name) + "_" + str(self.count).zfill(3) + ".jpg")
        except:
            pass


name = input("Image title: ")
create_directory(name)

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get(SITE)

# Find search box to input image's title
search_box = driver.find_element(By.CLASS_NAME, "gLFyf")
search_box.send_keys(name)
search_box.send_keys(Keys.ENTER)

# Scroll to the end for SCROLL_NUM times
last_height = driver.execute_script("return document.body.scrollHeight")
for _ in range(SCROLL_NUM):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # Wait the site to load more images
    sleep(1)

    new_height = driver.execute_script("return document.body.scrollHeight")
    
    # If there is any new image
    if new_height == last_height:
        try:
            driver.find_element(By.CSS_SELECTOR, ".mye4qd").click() # Click on "Show more" button
        except:
            break # Or break if can't load more
    last_height = new_height

images = driver.find_elements(By.CLASS_NAME, "YQ4gaf")

image_threads = []
for i, image in enumerate(images):
    image_thread = Image(image, i, name)
    image_threads.append(image_thread)
    image_thread.start()

for thread in image_threads:
    thread.join()

driver.close()