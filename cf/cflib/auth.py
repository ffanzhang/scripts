import os
import requests
import pickle
from datetime import datetime

from .parser import FormExtractor
from .config import *

def get_form(html, attrs):
    parser = FormExtractor(attrs)
    parser.feed(html)
    data = parser.get_data()
    parser.close()
    return data

def clear_cookies():
    try:
        os.remove(COOKIES)
    except:
        pass

def save_cookies(session):
    with open(COOKIES, 'wb+') as f:
        pickle.dump(session.cookies, f)
        os.fsync(f)

def load_cookies(): 
    try:
        with open(COOKIES, 'rb') as f:
            return pickle.load(f)
    except:
        return None

def cookies_expired(cookies):
    if cookies is None:
        return True
    current_time = datetime.utcnow().timestamp()
    for cookie in cookies:
        # if cookies expire in less than a day then we
        # should refresh cookies
        if cookie.expires is not None and \
            cookie.expires < current_time + 24 * 3600:
            return True
    return False

def session_from_cookies(cookies):
    session = requests.Session()
    session.cookies.update(cookies)
    return session

def save_last_user(handle):
    with open(HANDLE, 'w') as f:
        f.write(handle)
        os.fsync(f)

def get_last_user():
    try:
        with open(HANDLE, 'r') as f:
            return f.read().strip()
    except:
        return None

def login(handle, password):
    session = requests.Session()
    res = session.get(LOGIN_URL)
    assert res.status_code == 200, "Error getting login page"
    login_data = get_form(res.text, [("id", LOGIN_FORM_ID)])
    login_data[LOGIN_INPUT_NAME] = handle 
    login_data[LOGIN_PASSWORD_NAME] = password 
    res = session.post(LOGIN_URL, files=login_data)
    assert res.status_code == 200, "Error submitting login data"
    return session

def submit(session, id, index, lang_id, file_name, mode):
    url = "" 
    mode = mode.lower().strip()
    if mode == 'p':
        url = SUBMIT_URL
    elif mode == 'g':
        url = GYM_SUBMIT_URL.format(id)
    else:
        url = CONTEST_SUBMIT_URL.format(id)

    submit_page = session.get(url)
    submit_content = get_form(submit_page.text, [("class", SUBMIT_FORM_CLASS)])

    if mode == 'p':
        submit_content['submittedProblemCode'] = id + index 
    else:
        submit_content['submittedProblemIndex'] = index

    submit_content['programTypeId'] = lang_id 
    submit_content['source'] = open(file_name, 'r') 
    session.post(url, files=submit_content)
