#!/usr/bin/python3
import requests
from parser import FormExtractor

LOGIN_FORM_ID = "enterForm"
LOGIN_INPUT_NAME = "handleOrEmail"
LOGIN_PASSWORD_NAME = "password"
SUBMIT_FORM_CLASS = "submit-form"
LOGIN_URL = "http://codeforces.com/enter"
SUBMIT_URL = "http://codeforces.com/problemset/submit"
GYM_SUBMIT_URL = "http://codeforces.com/gym/{0}/submit"
CONTEST_SUBMIT_URL = "http://codeforces.com/contest/{0}/submit"

def get_form(html, attrs):
    parser = FormExtractor(attrs)
    parser.feed(html)
    data = parser.get_data()
    parser.close()
    return data

def get_session(handle, password):
    session = requests.Session()
    res = session.get(LOGIN_URL)
    login_data = get_form(res.text, [("id", LOGIN_FORM_ID)])
    login_data[LOGIN_INPUT_NAME] = handle 
    login_data[LOGIN_PASSWORD_NAME] = password 
    print(login_data)
    session.post(LOGIN_URL, files=login_data)
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
