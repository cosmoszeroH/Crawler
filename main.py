from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
import os


def create_project_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


site = "https://scholar.google.com/"

name = input("Author's full name: ")

df1 = pd.DataFrame({"Paper name": [],
                    "Link": [],
                    "Authors": [],
                    "Year": [],
                    "Source": [],
                    "Cited": [],
                    "Description": []})

name2 = '"' + name + '"'

edgeOption = Options()
edgeOption.add_experimental_option('excludeSwitches', ['enable-logging'])
edgeOption.add_argument("--lang=vi")
browser = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=edgeOption)
browser.get("https://scholar.google.com/")

browser.find_element(By.ID, 'gs_hdr_mnu').click()

sleep(1)

browser.find_element(By.XPATH, '/html/body/div/div[6]/div/div[2]/div[2]/a').click()

name_search = browser.find_element(By.XPATH, '/html/body/div/div[4]/div/div[2]/form/div[7]/div[2]/div[1]/input')
name_search.send_keys(name2)

name_search.send_keys(Keys.ENTER)

browser.find_element(By.CLASS_NAME, 'gs_rt2').find_element(By.TAG_NAME, 'a').click()

x = browser.find_element(By.ID, 'gsc_bpf_more')

while x.is_enabled():
    x.click()

sleep(1)

soup = BeautifulSoup(browser.page_source, 'html.parser')
items = soup.find_all('tr', {'class': 'gsc_a_tr'})

for each in items:
    try:
        paper_name = each.find('a', {'class': 'gsc_a_at'}).text
        link = each.find('a', {'class': 'gsc_a_at'}, href=True)
        link = site + link['href']

        browser2 = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=edgeOption)
        browser2.get(link)

        soup2 = BeautifulSoup(browser2.page_source, 'html.parser')
        children = soup2.findChildren("div", {'class': 'gs_scl'})
        authors = ''
        description = ''
        for child in children:
            if child.find('div', {'class': 'gsc_oci_field'}).text == "Tác giả":
                authors = child.find('div', {'class': 'gsc_oci_value'}).text
            elif child.find('div', {'class': 'gsc_oci_field'}).text == "Mô tả":
                description = child.find('div', {'class': 'gsc_oci_value'}).text

        sleep(0.5)
        browser2.close()

        children2 = each.findChildren("div", {'class': 'gs_gray'})

        source = children2[1].text
        count = each.find('a', {'class': 'gsc_a_ac gs_ibl'}).text
        year = each.find('span', {'class': 'gsc_a_h gsc_a_hc gs_ibl'}).text

        df2 = pd.DataFrame({"Paper name": [str(paper_name)],
                            "Link": [str(link)],
                            "Authors": [str(authors)],
                            "Year": [str(year)],
                            "Source": [str(source)],
                            "Cited": [str(count)],
                            "Description": [str(description)]})

        df1 = pd.concat([df1, df2], axis=0, ignore_index=True)

    except:
        pass

create_project_dir('paper')

df1.to_csv("papers/" + name + ".csv", index_label="No.")
sleep(2)
browser.close()
