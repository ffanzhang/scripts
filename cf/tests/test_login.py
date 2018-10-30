import unittest
import cflib.login as login
from cflib.config import * 
import requests
import requests_mock
import os

class TestLoginMethods(unittest.TestCase):
    _get_html = ""
    _post_html = ""
    def setUp(self):
        cur_path = os.path.dirname(__file__)

        get_fname = os.path.join(cur_path, "login_page.html")
        get_file = open(get_fname, 'r')
        self._get_html = get_file.read()

        post_fname = os.path.join(cur_path, "login_success.html")
        post_file = open(post_fname, 'r')
        self._post_html = post_file.read()

    def test_login(self):
        with requests_mock.Mocker() as mocker:
            mocker.get(LOGIN_URL, text=self._get_html)
            mocker.post(LOGIN_URL, text=self._post_html)
            session = login("username", "password")
            pass

if __name__ == '__main__':
    unittest.main()
