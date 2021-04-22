# Yacrawler - Yet Another Crawler
 Given a starting URL, the crawler will visit each URL it finds on the same domain.
 It should print each URL visited, and a list of links found on that page.
 The crawler limits itself to the subdomain of the starting url.

 # Design
The Crawler crawls a url in a recursive and concurrent way.
It uses python multiprocessing package to utilize a multicore architecture with the number of concurrent processes matching the number of the cores of the hosting platform.

The algorithm (method `crawl()`) starts by adding in the todo list the initial url and having that todo list to feed a pool of scraping processes. 

Every scrape process is assigned a single url that it gets out of todo list.

It then scrapes the page at that url using beatifulsoup to parse it and adds the same domain links found in a todo list that it returns back together with the rest of the links it found.

New todo links are appended in the global todo list for future scrape process to grab.

A dictinary (visited) marks off urls that have been already visited so that we don't revisit them in the event of them being present in a deeper level url.

The process ends when no urls are left in the global todo list.

# Preconditions 
- [Python 3.7+ and pip](https://docs.python-guide.org/dev/virtualenvs/#make-sure-you-ve-got-python-pip)
- [virtualenv](https://docs.python-guide.org/dev/virtualenvs/#lower-level-virtualenv)

# How to setup / Example run
`bash setup.sh` : This will create a python virtual env, install a few dependencies in it and activate it.
`python -m yacrawler https://docs.python.org` : This will start a crawler on `https://docs.python.org` to which you should start seeing output like:
```
(venv) yacrawler$ python -m yacrawler https://docs.python.org
https://docs.python.org
	https://www.python.org/
	https://devguide.python.org/docquality/#helping-with-documentation
	https://docs.python.org/3.10/
	https://docs.python.org/3.9/
	https://docs.python.org/3.8/
	https://docs.python.org/3.7/
	https://docs.python.org/3.6/
	https://docs.python.org/3.5/
	https://docs.python.org/2.7/
	https://www.python.org/doc/versions/
	https://www.python.org/dev/peps/
	https://wiki.python.org/moin/BeginnersGuide
	https://wiki.python.org/moin/PythonBooks
```
