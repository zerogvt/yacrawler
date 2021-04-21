# -*- coding: utf-8 -*-
from yacrawler.yacrawler import same_domain, rm_www_prefix, to_str, eat

import unittest
from unittest.mock import patch, Mock


class YacrawlerTest(unittest.TestCase):
    """Basic test cases."""

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

    def test_links_to_str(self):
        links = {"url": "domain.com", "links": ["one", "two", "three"]}
        want = "domain.com\n\tone\n\ttwo\n\tthree"
        self.assertEqual(to_str(links), want)

    @patch("yacrawler", "BeautifulSoup")
    def test_eat(self, m_bs):
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
