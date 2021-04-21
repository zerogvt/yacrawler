# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from requests import get, HTTPError
import validators
from urllib.parse import urlparse
from multiprocessing import Pool, active_children, Queue, Manager, cpu_count


def rm_www_prefix(text):
    prefix = "www."
    if text.startswith(prefix):
        return text[len(prefix) :]
    return text


def same_domain(url1, url2):
    dom1 = urlparse(url1).netloc
    dom2 = urlparse(url2).netloc
    return rm_www_prefix(dom1) == rm_www_prefix(dom2)


def cook(url):
    try:
        page = get(url)
        soup = BeautifulSoup(page.text, features="html.parser")
    except HTTPError:
        return None
    return soup


def eat(url, soup):
    if not soup:
        return None
    res = {"url": url, "links": [], "todo": []}
    for link in soup.find_all("a"):
        link_href = link.get("href")
        try:
            if validators.url(link_href):
                if same_domain(link_href, url):
                    res["todo"].append(link_href)
                res["links"].append(link_href)
        except TypeError:
            pass
    print(to_str(res), flush=True)
    return res


def scrape(url):
    res = eat(url, cook(url))
    if res:
        print(to_str(res), flush=True)
    return res


def to_str(links):
    outp = []
    outp.append(links["url"])
    for sub in links["links"]:
        outp.append(f"\t{sub}")
    return "\n".join(outp)


def crawl(url):
    todo = [url]
    visited = {}
    links = {}
    with Pool(processes=cpu_count()) as pool:
        while todo:
            results = pool.map(scrape, todo)
            todo.clear()
            for res in results:
                visited[res["url"]] = True
                links[res["url"]] = res["links"]
                for url in res["todo"]:
                    if url not in visited and url not in todo:
                        todo.append(url)
