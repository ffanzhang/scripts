import requests
import sys
from time import sleep
from threading import Timer
from .config import STATUS_URL
if sys.version_info[0] >= 3:
    import queue
else:
    import Queue as queue

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
        return str(s['problem']['index']) + " " + s['problem']['name'] + " " + \
            '{:>20}'.format(s['verdict'] + "(" + str(s['passedTestCount'] + 1) + ") ") + \
            str(s['timeConsumedMillis']) + " ms", s['verdict'] == 'TESTING'
    except:
        return None

def query_status(*args):
    handle = args[0] 
    q = args[1]
    try:
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
    except:
        q.put("Unknown Error")

def get_submit_status(handle, interval):
    sch = Scheduler(interval, query_status, handle)
    sch.gogogo()
