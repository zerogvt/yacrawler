# -*- coding: utf-8 -*-
"""
Crawl a url in a concurrent way.
Concurrent processes will match the number of the cores
of the hosting platform.

See function crawl() for design specs.
"""
from bs4 import BeautifulSoup
from requests import get, HTTPError
import validators
from urllib.parse import urlparse
from multiprocessing import Pool, active_children, Queue, Manager, cpu_count


def rm_www_prefix(text):
    """
    Remove www prefix
    """
    prefix = "www."
    if text.startswith(prefix):
        return text[len(prefix) :]
    return text


def same_domain(url1, url2):
    """
    Return True if the two urls belong at the same domain.
    """
    if not url1 or not url2:
        return False
    dom1 = urlparse(url1).netloc
    dom2 = urlparse(url2).netloc
    return rm_www_prefix(dom1) == rm_www_prefix(dom2)


def to_str(links):
    outp = []
    outp.append(links["url"])
    for sub in links["links"]:
        outp.append(f"\t{sub}")
    return "\n".join(outp)


def cook(url):
    """HTTP Get page at url and parse it with BeatifulSoup"""
    try:
        page = get(url)
        soup = BeautifulSoup(page.text, features="html.parser")
    except HTTPError:
        return None
    return soup


def eat(url, soup):
    """
    Analyze a beatiful soup for links.
    Keep same domain links in a todo list as we'll have to crawl
    them at a later step.
    """
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
    return res


def scrape(url):
    """
    Scrape a specific url for links.
    Wrapper around eat and cook methods.
    """
    res = eat(url, cook(url))
    if res:
        print(to_str(res), flush=True)
    return res


def crawl(url):
    """
    Crawl a url in a recursive and concurrent way.
    Number of concurrent processes will match the number of the cores of the
    hosting platform.
    The algorithm starts by adding in the todo list the initial url and having
    that todo list to feed a pool of scraping processes.
    Every scrape process is assigned a single url that it gets out of todo list.
    It then adds the same domain links found in a todo list that it returns back
    together with the rest of the links it found.
    New todo links are appended in the global todo list for future scrape process.
    A dictinary (visited) marks off urls that have been already visited so that
    we don't revisit them in the event of them being present in a deeper level
    url.
    """
    todo = [url]
    visited = {}
    links = {}
    with Pool(processes=cpu_count()) as pool:
        while todo:
            results = pool.map(scrape, todo)
            todo.clear()
            for res in results:
                visited[res["url"]] = True
                links[res["url"]] = {"url": res["url"], "links": res["links"]}
                for url in res["todo"]:
                    if url not in visited and url not in todo:
                        todo.append(url)
    return links
