import requests
import sys
from time import sleep
from threading import Timer
import queue
from .config import STATUS_URL

class Scheduler():
    _handle = None
    _interval = None
    _func = None
    _queue = None
    def __init__(self, interval, func, handle):
        self._handle = handle
        self._interval = interval
        self._func = func
        self._queue = queue.Queue()

    def gogogo(self):
        while True:
            timer = Timer(self._interval, self._func, [self._handle, \
                                                       self._queue])
            timer.start()
            timer.join()
            if self._queue.qsize() > 0:
                timer.cancel()
                return

def parse_submit_status(data):
    try:
        data = data.json()['result']
        s = data[0]
        return str(s['problem']['contestId']) + s['problem']['index'] + " " + \
            '{:>20}'.format(s['verdict'] + "(" + str(s['passedTestCount'] + 1) + ") ") + \
            str(s['timeConsumedMillis']) + " ms", s['verdict'] == 'TESTING'
    except:
        return None

def query_status(*args):
    handle = args[0] 
    q = args[1]
    data = requests.get(STATUS_URL.format(handle))
    if data.status_code != 200:
        q.put("Error Code: " + str(data.status_code))
        return

    datastr, testing = parse_submit_status(data)
    sys.stdout.write(datastr + '\n')
    if datastr == None:
        q.put("Error Parsing")
        return

    if testing == False:
        q.put("Done")
        return

def get_submit_status(handle, interval):
    sch = Scheduler(interval, query_status, handle)
    sch.gogogo()
