import os

from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from . import helper

import time
import pandas as pd

scrap_interval = 60  # seconds
request_interval = 3  # seconds
site_url = 'http://www.aljazeera.com'
raw_html = 'output/html/aj'


class Scrapper:
    _url = ''
    _data = ''
    _log = None
    _soup = None
    articles = []
    menu_url_list = []
    articles_data = []
    http_exception = False
    count = 0
    script_filename = "(" + os.path.basename(__file__) + ")"

    def __init__(self, url, log):
        self._url = url
        self._log = log

    def retrieve_webpage(self):
        try:
            self.http_exception = False
            self._log.info(self.script_filename + "Opening the Url: " + self._url)
            html = urlopen(self._url)
        except HTTPError as e:
            if e.code == 404:
                self.http_exception = True
            print(e)
            self._log.report(str(e))
        except Exception as e:
            print(e)
            self._log.report(str(e))
        else:
            self.count += 1
            self._log.info(self.script_filename + "Data read from html Url: " + self._url)
            self._data = html.read()
            if len(self._data) > 0:
                print("Retrieved successfully")

    def write_webpage_as_html(self, data=''):
        if data is '':
            data = self._data
        filepath = raw_html + str(self.count) + ".html"
        helper.write_webpage_as_html(filepath, data)

    def read_webpage_from_html(self):
        self._log.info(self.script_filename + "Reading web page from html....")
        filepath = raw_html + str(self.count) + ".html"
        self._data = helper.read_webpage_from_html(filepath)

    def change_url(self, url):
        self._url = url
        self._log.info(self.script_filename + "Url Changes to: " + url)

    def convert_data_to_bs4(self):
        self._soup = BeautifulSoup(self._data, "html.parser")
        self._log.info(self.script_filename + "Data setup for beautiful soup")

    def parse_soup_to_find_main_pages(self):
        self._log.info(self.script_filename + "#### scrapping nav bar and drop down items of title page ####")
        menu_divs = self._soup.find_all('li', attrs={"class": "col-sm-4"})
        for tag in menu_divs:
            menu_lists = tag.find_all('a')
            for linktag in menu_lists:
                if linktag.get('href'):
                    # print (self._url + tag.parent.get('href'), tag.string)
                    link = site_url + linktag.get('href')
                    if self.find_url_not_in_list(link, self.menu_url_list):
                        data_art = [link, 0]
                        self.menu_url_list.append(data_art)

    def write_menu_list_to_file(self):
        self._log.info(self.script_filename + "#### Writing the menu urls to file ####")
        try:
            pdwrite = pd.DataFrame(self.menu_url_list)
            pdwrite.to_csv("output/menu_url.csv", encoding='utf-8', header=False, index=False)
        except Exception as e:
            print(e)
            self._log.report(e)
            return False
        else:
            return True

    def parse_soup_to_extract_urls(self):
        self._log.info(self.script_filename + "#### scrapping article urls from a page ####")
        browser = webdriver.Chrome('chromedriver.exe')
        wait = WebDriverWait(browser, 20)
        browser.get(self._url)
        no_of_clicks = 1
        while True:
            try:
                self._log.info(self.script_filename + "Waiting to find element .. Show More")
                show_more = wait.until(
                    EC.element_to_be_clickable((By.XPATH, '//button[@type="button"][contains(.,"Show More")]')))
                self._log.info(self.script_filename + "Waiting to find element .. Clicking Button")
                browser.execute_script("arguments[0].click();", show_more)
                time.sleep(3)
                if no_of_clicks >= 2:
                    break
                no_of_clicks += 1
            except Exception as e:
                print(e)
                self._log.report(e)
                break

        self._soup = BeautifulSoup(browser.page_source, 'html.parser')
        browser.close()
        news_list = self._soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])  # h1

        self._log.info(self.script_filename + "Finding all the headings from a page")
        for tag in news_list:
            if tag.parent.get('href'):
                # print (self._url + tag.parent.get('href'), tag.string)
                link = tag.parent.get('href')
                if ("comhttps:" not in link) and ("comhttp:" not in link):
                    link = site_url + link
                if self.find_url_not_in_list(link, self.articles):
                    data_art = [link, 0]
                    self.articles.append(data_art)

    def parse_soup_to_extract_data(self):
        self._log.info(self.script_filename + "#### scrapping author name, title, tags from an article ####")
        author_div = self._soup.find_all('div', attrs={"class": ("article-heading-author-name")})
        author_name = "AL JAZEERA NEWS"
        names = []
        for div in author_div:
            raw_tags = div.find_all('a')
            for link in raw_tags:
                names.append(link.get_text())
            names = list(filter(None, names))
        if names:
            author_name = (','.join(names))
        self._log.info(self.script_filename + "## Names Scrapeed ##")

        title = self._soup.find('title').get_text()
        self._log.info(self.script_filename + "## Title Scrapeed ##")

        tags = []
        refinedata = self._soup.find_all('ul', attrs={"class": ("article-topic-detail-list")})
        for divs in refinedata:
            raw_tags = divs.find_all('a')
            for link in raw_tags:
                tags.append(link.get_text())
        self._log.info(self.script_filename + "## Tags Scrapeed ##")

        extracted_data = [self._url, title, author_name, (','.join(tags))]
        if extracted_data not in self.articles_data:
            self.articles_data.append(extracted_data)

    def find_url_not_in_list(self, url, urls_list):
        for link in urls_list:
            if str(link[0]) == url:
                self._log.info(self.script_filename + "DISCARDING DUPLICATE URL:" + url)
                return False
        return True
