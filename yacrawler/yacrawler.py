# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from requests import get
import validators
from urllib.parse import urlparse


class Crawler:
    def __init__(self, urls):
        self.urls = urls
        self.visited = set()
        self.res = {}

    def crawl(self):
        for url in self.urls:
            self.scrape(url)
        self.print_res()

    def scrape(self, url):
        self.res[url] = []
        my_domain = urlparse(url).netloc
        print(".", end="", flush=True)
        page = get(url)
        soup = BeautifulSoup(page.text, features="html.parser")
        for link in soup.find_all("a"):
            link_href = link.get('href')
            try:
                if validators.url(link_href):
                    if urlparse(link_href).netloc == my_domain:
                        if link_href not in self.visited:
                            self.scrape(link_href)
                    self.res[url].append(link_href)
            except TypeError:
                pass
        print("")

    def print_res(self):
        for url in self.res:
            print(url)
            for sub in self.res[url]:
                print(f"\t{sub}")
        print("")
