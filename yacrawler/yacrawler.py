# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

class Crawler():
    def __init__(self, urls):
        self.urls = urls

    def crawl(self):
        for url in self.urls:
            print(url)
