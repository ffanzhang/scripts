from cflib.config import * 
import cflib.auth as auth
import requests
import os
import pickle

import unittest
from unittest import mock

class MockResponse(object):
    def __init__(self, text, cookies={}):
        self.status_code = 200
        self.text = text
        self.cookies = cookies

class TestLogin(unittest.TestCase):
    _get_html = ""
    _post_html = ""
    _cookies = None
    def setUp(self):
        cur_path = os.path.dirname(__file__)

        get_fname = os.path.join(cur_path, "login_page.html")
        with open(get_fname, 'r') as get_file:
            self._get_html = get_file.read()

        post_fname = os.path.join(cur_path, "login_success.html")
        with open(post_fname, 'r') as post_file:
            self._post_html = post_file.read()

        cookies_fname = os.path.join(cur_path, "sample_cookies")
        with open(cookies_fname, 'rb') as cookies_file:
            self._cookies = pickle.load(cookies_file)

    @mock.patch('requests.Session')
    def test_login_fails(self, mock_session):
        get_response = MockResponse(self._get_html)
        post_response = MockResponse(self._post_html)
        mock_session.return_value = \
            mock.MagicMock(get=mock.MagicMock(return_value=get_response), \
                           post=mock.MagicMock(return_value=post_response),
                           cookies=None)
        try:
            session = auth.login("username", "wrongpassword")
            self.fail("Expected login to fail")
        except:
            pass

    @mock.patch('requests.Session')
    def test_login_succeeds(self, mock_session):
        get_response = MockResponse(self._get_html)
        post_response = MockResponse(self._post_html)
        mock_session.return_value = \
            mock.MagicMock(get=mock.MagicMock(return_value=get_response), \
                           post=mock.MagicMock(return_value=post_response),
                           cookies=self._cookies)
        try:
            session = auth.login("username", "password")
        except:
            self.fail("Expected login to succeed")
            pass

if __name__ == '__main__':
    unittest.main()
