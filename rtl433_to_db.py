#!/usr/bin/python

import subprocess
import time
from datetime import datetime
import threading
import Queue
import shlex
import json
import urllib2


class AsynchronousFileReader(threading.Thread):
    def __init__(self, fd, queue):
        assert isinstance(queue, Queue.Queue)
        assert callable(fd.readline)
        threading.Thread.__init__(self)
        self._fd = fd
        self._queue = queue

    def run(self):
        for line in iter(self._fd.readline, ''):
            self._queue.put(line)

    def eof(self):
        return not self.is_alive() and self._queue.empty()

def startsubprocess(command):

    sCmd = shlex.split(command)
    process = subprocess.Popen(sCmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout_queue = Queue.Queue()
    stdout_reader = AsynchronousFileReader(process.stdout, stdout_queue)
    stdout_reader.start()
    stderr_queue = Queue.Queue()
    stderr_reader = AsynchronousFileReader(process.stderr, stderr_queue)
    stderr_reader.start()
    i = 0

    # Only publish if it has been at least this many seconds
    limit = 60
    tStamp = ""

    # keep track of recent ID / temperatures to prevent republishing
    historyDic = {}

    # publish or not flag
    publish = 0

    while not stdout_reader.eof() or not stderr_reader.eof():
        while not stdout_queue.empty():
            line = stdout_queue.get()
            publish = 0
            try:
            jData = json.loads(line)
            except ValueError, e:
                # Output the line if we can't parse to JSON
                print line
            else:

                # Convert the time provided by rtl_433 to a timestamp
                thisDateTime = datetime.strptime(jData['time'], '%Y-%m-%d %H:%M:%S')
                thisTimestamp = time.mktime(thisDateTime.timetuple())

                # the ID reported by rtl_433 for this particular thermometer
                thisId = jData['id']

                # Check to see if we have seen this ID before, and if so, have we met the minimum delay to publush another?
                if thisId in historyDic:
                    lastTimestamp = historyDic[thisId]
                    if (thisTimestamp - lastTimestamp) > limit:
                        publish = 1
                else:
                     publish = 1

                # if the test for publishing is met, do the publish operation
                if publish == 1:
                     publish = 0
                     req = urllib2.Request('http://<YOUR_URL>/envTrack.php')
                     req.add_header('Content-Type', 'application/x-www-form-urlencoded')
                     response = urllib2.urlopen(req, json.dumps(jData))
                     result = response.read()
                     # store this published result in our history dictionary
                     historyDic[thisId] = thisTimestamp

        # pause at least 1/10s before checking for more data
        time.sleep(.1)

    stdout_reader.join()
    stderr_reader.join()

    process.stdout.close()
    process.stderr.close()

if __name__ == '__main__':

    startsubprocess("rtl_433 -R 39 -q -F json")
    print("Exiting...")
