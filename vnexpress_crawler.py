# Used to crawl news from VNExpress website

import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

from threading import Thread
from bs4 import BeautifulSoup
from time import sleep

from utils import create_directory, create_csv_file


SITE = 'https://vnexpress.net/'

DIR_PATH = r'./vnexpress'
create_directory(DIR_PATH)


# Using thread to boost the crawl speed
# The class accesses to the link of news and get information
class News(Thread):
    def __init__(self, link, count):
        super().__init__()
        self.link = link
        self.count = count

    def run(self):
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        try:
            driver.get(self.link)
        except:
            return
        
        # Get the title
        try:
            title = driver.find_element(By.CLASS_NAME, 'title-detail').text
        except:
            title = driver.find_element(By.CLASS_NAME, 'title-news').text

        # Get the date
        date = driver.find_element(By.CLASS_NAME, 'date').text

        # Get the summary
        description = driver.find_element(By.CLASS_NAME, 'description').text

        # Save all the above information to a txt file
        with open(DIR_PATH + "/" + str(i).zfill(3) + ".txt", "a+", encoding="utf-8") as f:
            f.write("Title: " + title)
            f.write("\n\n")
            f.write("Date: " + date)
            f.write("\n\n")
            f.write("Description :" + description)

        # Get comments on the news
        df = pd.DataFrame({"Author": [],
                        "Comment": []})
        
        # Get the show_more_comment button
        show_more_comment = driver.find_elements(By.ID, "#show_more_coment")
        # Show all comments
        while show_more_comment.is_enabled():
            show_more_comment[-1].click()

        # Get name of who commented and the content
        comments = driver.find_elements(By.CLASS_NAME, 'full_content')
        
        for comment in comments:
            author_comment = comment.find_element(By.TAG_NAME, 'b').text
            content_comment = comment.text
            content_comment = content_comment[len(author_comment) + len('\n'):]\
            
            df_temp = pd.DataFrame({"Author": [author_comment],
                                "Comment": [content_comment]})
            df = pd.concat([df, df_temp], axis=0, ignore_index=True)

        # Save the above information to csv file
        df.to_csv(DIR_PATH + "/" + str(self.count).zfill(3) + ".csv", index_label="No.")
        driver.close()
        
        


driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get(SITE)

# Get links of news
title_news_links = []
title_news_list = driver.find_elements(By.CLASS_NAME, "title-news")
for title_news in title_news_list:
    title_news_links.append(title_news.find_element(By.TAG_NAME, 'a').get_attribute("href"))

news_threads = []
for i, link in enumerate(title_news_links):
    news = News(link, i)
    news_threads.append(news)
    news.start()

for thread in news_threads:
    thread.join()

driver.close()

