# python tests.py test_not_framework
import unittest

from not_django import find_match, Response


class TestCase(unittest.TestCase):

    def test_find_match(self):
        dynamic_urls = [
          ('/stat/[0-9]+/$', 'stat_func'),
          ('/ajax/region/[0-9]+/$', 'ajax'),
        ]
        func, param = find_match('xxx', dynamic_urls)
        self.assertEqual(param, None)

        func, param = find_match('/stat/555/', dynamic_urls)
        self.assertEqual(func, 'stat_func')
        self.assertEqual(param[0], 555)

        func, param = find_match('/stat/55x/', dynamic_urls)
        self.assertEqual(param, None)

        func, param = find_match('/ajax/region/777/', dynamic_urls)
        self.assertEqual(func, 'ajax')
        self.assertEqual(param[0], 777)

    def test_Response(self):
        r = Response()
        self.assertEqual(r.status, '200 OK')
