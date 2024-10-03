# Used to crawl articles of a particular author from Google Scholar website

import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

from threading import Thread

from bs4 import BeautifulSoup

from time import sleep

from utils import create_csv_file        


SITE = r"https://scholar.google.com/"


# Using thread to boost the crawl speed
class Paper(Thread):
    def __init__(self, paper):
        super().__init__()
        self.paper = paper
        self.df = None # All information relating to paper will stored in this attribute

    def run(self):
        try:
            paper_name = paper.find('a', {'class': 'gsc_a_at'}).text
            
            # Access the paper site to get information about authors and description
            paper_link = paper.find('a', {'class': 'gsc_a_at'}, href=True)
            paper_link = SITE + paper_link['href']

            paper_driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
            paper_driver.get(paper_link)

            paper_soup = BeautifulSoup(paper_driver.page_source, 'html.parser')

            # Get authors and description of the paper
            children = paper_soup.findChildren("div", {'class': 'gs_scl'}) # Get all information section
            authors = ''
            description = ''
            for child in children:
                if child.find('div', {'class': 'gsc_oci_field'}).text == "Authors":
                    authors = child.find('div', {'class': 'gsc_oci_value'}).text
                elif child.find('div', {'class': 'gsc_oci_field'}).text == "Description":
                    description = child.find('div', {'class': 'gsc_oci_value'}).text

            paper_driver.close()

            # Get source, cited and year
            children = paper.findChildren("div", {'class': 'gs_gray'})

            source = children[1].text
            cited = paper.find('a', {'class': 'gsc_a_ac gs_ibl'}).text
            year = paper.find('span', {'class': 'gsc_a_h gsc_a_hc gs_ibl'}).text

            self.df = pd.DataFrame({"Paper name": [str(paper_name)],
                                "Link": [str(paper_link)],
                                "Authors": [str(authors)],
                                "Year": [str(year)],
                                "Source": [str(source)],
                                "Cited": [str(cited)],
                                "Description": [str(description)]})
        except:
            pass


name = input("Author's full name: ")

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get(SITE)

df = pd.DataFrame({"Paper name": [],
                    "Link": [],
                    "Authors": [],
                    "Year": [],
                    "Source": [],
                    "Cited": [],
                    "Description": []})

# Find in "Advanced search"
driver.find_element(By.ID, 'gs_hdr_mnu').click() # Click on the menu symbol
# Search by author in "Return articles authored by"
driver.find_element(By.XPATH, '/html/body/div/div[6]/div/div[2]/div[2]/a').click()
name_search = driver.find_element(By.XPATH, '/html/body/div/div[4]/div/div[2]/form/div[7]/div[2]/div[1]/input')
name_search.send_keys(name)
name_search.send_keys(Keys.ENTER)

# Choose the first link to the author site
driver.find_element(By.CLASS_NAME, 'gs_rt2').find_element(By.TAG_NAME, 'a').click()
sleep(1)

# Show all papers
show_more = driver.find_element(By.ID, 'gsc_bpf_more')
while show_more.is_enabled():
    show_more.click()
    sleep(1)

soup = BeautifulSoup(driver.page_source, 'html.parser')

# Get all papers
papers = soup.find_all('tr', {'class': 'gsc_a_tr'})

paper_threads = []
for paper in papers:
    paper_thread = Paper(paper)
    paper_threads.append(paper_thread)
    paper_thread.start()

for paper_thread in paper_threads:
    paper_thread.join()
    df = pd.concat([df, paper_thread.df], axis=0, ignore_index=True)

create_csv_file(df, name)

driver.close()