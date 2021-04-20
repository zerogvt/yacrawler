import sys
from .yacrawler import Crawler

Crawler(urls=sys.argv[1:]).crawl()
