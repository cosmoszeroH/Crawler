import os
import pandas as pd
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager


def create_project_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


dir_name = 'vnexpress'
create_project_dir(dir_name)

browser = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
browser.get("https://vnexpress.net/")
sleep(3)

# Lay cac bai bao
title_news_links = []
title_news_list = browser.find_elements(By.CLASS_NAME, "title-news")
for title_news in title_news_list:
    title_news_links.append(title_news.find_element(By.TAG_NAME, 'a').get_attribute("href"))
browser.close()

# Lay thong tin trong bai
i = 0
for title_news_link in title_news_links:
    df1 = pd.DataFrame({"Author": [],
                        "Comment": []})

    browser = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
    try:
        browser.get(title_news_link)
    except:
        continue

    # Lấy ten bai bao
    try:
        show_title = browser.find_element(By.CLASS_NAME, 'title-detail').text
    except:
        show_title = browser.find_element(By.CLASS_NAME, 'title-news').text

    # Lay ngay dang bai
    show_date = browser.find_element(By.CLASS_NAME, 'date').text

    # Lay noi dung tom tat
    show_description = browser.find_element(By.CLASS_NAME, 'description').text
    with open(dir_name + "/" + str(i).zfill(3) + ".txt", "a+", encoding="utf-8") as f:
        f.write("Title: " + show_title)
        f.write("\n\n")
        f.write("Date: " + show_date)
        f.write("\n\n")
        f.write("Description :" + show_description)

    # Lay show_more_comment
    try:
        browser.find_element(By.CSS_SELECTOR,
                             "#box_comment_vne > div > div.view_more_coment.width_common.mb10 > a").click()
        exist_show_more_cmt = True
    except:
        exist_show_more_cmt = False
    sleep(3)
    while exist_show_more_cmt:
        list1 = browser.find_elements(By.ID, "#show_more_coment")
        try:
            list1[-1].click()
        except:
            pass
        sleep(3)

        list2 = browser.find_elements(By.ID, "#show_more_coment")
        try:
            list2[-1].click()
        except:
            pass
        sleep(3)
        if len(list2) == len(list1):
            break

    # Lay ten nguoi comment va noi dung comment
    comments = browser.find_elements(By.CLASS_NAME, 'full_content')
    content_comments, author_comments = [], []
    for comment in comments:
        author_comment = comment.find_element(By.TAG_NAME, 'b').text
        content_comment = comment.text
        content_comment = content_comment[len(author_comment) + len('\n'):]
        df2 = pd.DataFrame({"Author": [author_comment],
                            "Comment": [content_comment]})
        df1 = pd.concat([df1, df2], axis=0, ignore_index=True)

    df1.to_csv(dir_name + "/" + str(i).zfill(3) + ".csv", index_label="No.")
    i += 1
    sleep(1)
    browser.close()
