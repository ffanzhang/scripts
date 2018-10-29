import requests
from time import sleep
import sys

def get_submit_status(session, handle, interval):
    while True:
        try:
            data = session.get("http://codeforces.com/api/user.status?handle=" + handle + "&from=1&count=" + str(1)).json()['result']
            s = data[0]
            print(str(s['problem']['contestId']) + s['problem']['index'] + " " + \
                '{:>20}'.format(s['verdict'] + "(" + str(s['passedTestCount'] + 1) + ") ") + str(s['timeConsumedMillis']) + " ms")
            if s['verdict'] != 'TESTING':
                break
        except:
            sleep(interval)
            continue
    sleep(interval)
