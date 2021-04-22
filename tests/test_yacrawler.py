# -*- coding: utf-8 -*-
from yacrawler.yacrawler import same_domain, rm_www_prefix, to_str, eat, cook, crawl
from bs4 import BeautifulSoup
import unittest
from unittest.mock import patch, Mock


class YacrawlerTest(unittest.TestCase):
    """Unit tests for yacrawler"""

    html_doc = """<html><head><title>The Dormouse's story</title></head>
                    <body>
                    <p class="title"><b>The Dormouse's story</b></p>

                    <p class="story">Once upon a time there were three little sisters; and their names were
                    <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
                    <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
                    <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
                    and they lived at the bottom of a well.</p>

                    <p class="story">...</p>
                    """

    def test_same_domain_ok(self):
        self.assertTrue(same_domain("http://www.domain.com", "http://domain.com"))
        self.assertTrue(same_domain("https://domain.com", "htpp://domain.com"))
        self.assertTrue(same_domain("http://www.domain.com", "htpps://domain.com"))
        self.assertTrue(
            same_domain("http://www.domain.com/path/path", "http://domain.com")
        )
        self.assertFalse(
            same_domain("http://www.domain.com", "http://another.dmain.com")
        )

    def test_same_domain_err(self):
        self.assertFalse(
            same_domain("http://www.domain.com", "http://another.dmain.com")
        )

    def test_remove_www_prefix(self):
        self.assertEqual(rm_www_prefix("www.domain.com"), "domain.com")

    def test_to_str(self):
        links = {"url": "domain.com", "links": ["one", "two", "three"]}
        want = "domain.com\n\tone\n\ttwo\n\tthree"
        self.assertEqual(to_str(links), want)

    def test_eat(self):
        url = "http://domain.com"
        soup = BeautifulSoup(self.html_doc, features="html.parser")
        have = eat(url, soup)
        want = {
            "url": "http://domain.com",
            "links": [
                "http://example.com/elsie",
                "http://example.com/lacie",
                "http://example.com/tillie",
            ],
            "todo": [],
        }
        self.assertEqual(want, have)

    @patch("yacrawler.yacrawler.get")
    def test_cook(self, m_get):
        class Page:
            def __init__(self, text):
                self.text = text

        m_get.return_value = Page(self.html_doc)
        soup = cook("doesntmatter.com")
        self.assertEqual(soup.title.string, "The Dormouse's story")

    @patch("yacrawler.yacrawler.Pool")
    def test_crawl(self, m_pool):
        url = "http://domain.com"
        m_pool_map = Mock()
        m_pool.return_value.__enter__.return_value.map = m_pool_map
        m_pool_map.return_value = [
            {
                "url": url,
                "links": [
                    "http://domain.com/1",
                    "http://domain.com/2",
                    "http://anotherdomain.com/1",
                ],
                "todo": [],
            }
        ]
        have = crawl(url)
        print(have)
        want = {
            url: {
                "url": url,
                "links": [
                    "http://domain.com/1",
                    "http://domain.com/2",
                    "http://anotherdomain.com/1",
                ],
            }
        }
        self.assertEqual(want, have)
