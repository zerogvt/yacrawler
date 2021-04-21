# -*- coding: utf-8 -*-
from yacrawler import yacrawler

import unittest


class YacrawlerTest(unittest.TestCase):
    """Basic test cases."""

    def test_same_domain(self):
        self.assertTrue('www.domain.com', 'domain.com')
        self.assertTrue('domain.com', 'domain.com')
        self.assertTrue('http://www.domain.com', 'domain.com')
        self.assertTrue('https://www.domain.com', 'domain.com')
        self.assertFalse('www.domain.com', 'another.dmain.com')
