# python tests.py test_urls
import unittest

from werkzeug.test import Client
from wsgi import wsgi_app


class TestCase(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.client = Client(wsgi_app)


class TestCaseGet(TestCase):

    def get(self, url, code):
        app_iter, status, headers = self.client.get(url)
        self.assertIn(str(code), status)
        return ''.join(app_iter)

    def test_404(self):
        self.get('/not_existing_url', 404)

    def test_root(self):
        html = self.get('/', 200)
        self.assertIn('<a href="/view/">', html)

    def test_comment(self):
        html = self.get('/comment/', 200)
        self.assertIn('Form for input comment will be here', html)

    def test_view(self):
        html = self.get('/view/', 200)
        self.assertIn('<a href="/comment/">Add new comment</a>', html)
        self.assertIn('<a href="/stat/">View statistics</a>', html)

    def test_stat(self):
        html = self.get('/stat/', 200)
        self.assertIn('Table of comment statistics will be here', html)

    def test_stat_region(self):
        html = self.get('/stat/555/', 200)
        self.assertIn('Not implemented yet', html)
        self.get('/stat/x55/', 404)

    def test_ajax_region(self):
        html = self.get('/ajax/region/555/', 200)
        self.assertIn('Not implemented yet', html)
        self.get('/ajax/region/x55/', 404)


class TestCasePost(TestCase):

    def post(self, url, data, code):
        app_iter, status, headers = self.client.post(url, data=data)
        self.assertIn(str(code), status)
        return ''.join(app_iter)

    def test_comment(self):
        html = self.post('/comment/', {'xxx': 'zzz'}, 200)
        self.assertIn('Not implemented yet', html)

    def test_view(self):
        html = self.post('/view/', {'xxx': 'zzz'}, 200)
        self.assertIn('Not implemented yet', html)
