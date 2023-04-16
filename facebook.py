import os
import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.microsoft import EdgeChromiumDriverManager


def create_project_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


DEPTH = 5

dir_name = 'facebook'
create_project_dir(dir_name)

browser = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
browser.get("https://www.facebook.com/UIT.Fanpage/")

for scroll in range(DEPTH):
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

post_lists = browser.find_elements(By.XPATH, "//a[@class = 'x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xt0b8zv xo1l8bm']")

post_links = []
for post in post_lists:
    post_links.append(post.get_attribute('href'))

browser.close()

i = 0
for post in post_links:
    browser = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
    try:
        browser.get(post)
    except:
        continue

    #show more content
    try:
        browser.find_element(By.CLASS_NAME, "x1gslohp").click()
    except:
        pass

    # get post content
    post_contents = browser.find_elements(By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div[2]/div/div/div/div/div/div/div/div[1]/div/div[2]/div[1]/div[2]/div[2]")
    for content in post_contents:
        with open(dir_name + "/" + str(i).zfill(3) + ".txt", "a+", encoding='utf-8') as f:
            f.write(content.text)

    # get comments
    try:
        browser.find_element(By.XPATH, "//*[@id='js_30']/a").click()
        time.sleep(3)
        print(1)
    except:
        df1 = pd.DataFrame({"Name": [],
                            "Comment": []})
        df1.to_csv(dir_name + "/" + str(i).zfill(3) + ".csv", index_label="No.")
        i += 1
        time.sleep(1)
        continue

    df1 = pd.DataFrame({"Name": [],
                        "Comment": []})
    j = 1
    while True:
        xpath = "//*[@id='u_0_g_dV']/div[2]/div[3]/ul/li[" + str(j) + "]"
        try:
            cmt = browser.find_element(By.XPATH, xpath)
        except:
            break
        name_xpath = xpath + "/div[1]/div/div[2]/div/div[1]/div[1]/div/div/div/div/div[2]/a"
        cmt_xpath = xpath + "/div[1]/div/div[2]/div/div[1]/div[1]/div/div/div/div/div[2]/span/span/span"

        name = browser.find_element(By.XPATH, name_xpath)
        cmt_content = browser.find_element(By.XPATH, cmt_xpath)

        df2 = pd.DataFrame({"Name": [name],
                            "Comment": [cmt_content]})

        df1 = pd.concat([df1, df2], axis=0, ignore_index=True)
        j += 1

    df1.to_csv(dir_name + "/" + str(i).zfill(3) + ".csv", index_label="No.")
    i += 1
    time.sleep(1)

    browser.close()


