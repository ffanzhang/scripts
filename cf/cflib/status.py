import requests
import sys
from time import sleep
from .config import STATUS_URL

class BadRequestException(Exception):
    pass

def get_submit_status(handle, interval):
    while True:
        try:
            data = requests.get(STATUS_URL.format(handle))
            if data.status_code == 400:
                raise BadRequestException

            data = data.json()['result']
            s = data[0]
            print(str(s['problem']['contestId']) + s['problem']['index'] + " " + \
                '{:>20}'.format(s['verdict'] + "(" + str(s['passedTestCount'] + 1) + ") ") + str(s['timeConsumedMillis']) + " ms")
            if s['verdict'] != 'TESTING':
                break
        except BadRequestException:
            print("Bad Request, most likely due to handle not found.")
            break
        except:
            # other errors are likely due to timeout
            sleep(interval)
            continue
        sleep(interval)
