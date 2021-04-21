# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from requests import get
import validators
from urllib.parse import urlparse
from multiprocessing import Pool, active_children, Queue, Manager

def remove_www_prefix(text):
    prefix = 'www.'
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

def same_domain(url1, url2):
    return remove_www_prefix(url1) == remove_www_prefix(url2)

def scrape(url):
    res = {'url': url, 'links': [], 'todo': []}
    links = []
    todo = []
    my_domain = urlparse(url).netloc
    page = get(url)
    soup = BeautifulSoup(page.text, features="html.parser")
    for link in soup.find_all("a"):
        link_href = link.get("href")
        try:
            if validators.url(link_href):
                if same_domain(urlparse(link_href).netloc, my_domain):
                    res['todo'].append(link_href)
                res['links'].append(link_href)
        except TypeError:
            pass
    print_links({url: res['links']})
    return res

def print_links(links):
    for url in links:
        print(url, flush=True)
        for sub in links[url]:
            print(f"\t{sub}", flush=True)
    print("")


def crawl(url):
    todo = [url]
    visited = {}
    links = {}
    with Pool(processes=4) as pool:
        while todo:
            results = pool.map(scrape, todo)
            todo.clear()
            for res in results:
                visited[res['url']] = True
                links[res['url']] = res['links']
                for url in res['todo']:
                    if url not in visited and url not in todo:
                        todo.append(url)
    # print_links(links)