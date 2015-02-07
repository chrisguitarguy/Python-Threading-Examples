# -*- coding: utf-8 -*-
"""
A simple threading example. Create some threads by subclassing `threading.Thread`,
keep track of them and wait for them to join.
"""

import random
import threading
import time


class SleepingThread(threading.Thread):

    #: How long we're going to sleep for
    sleep_length = None

    def __init__(self, sleep_length=None):
        super().__init__()
        self.sleep_length = sleep_length or random.randrange(1, 20)

    def run(self):
        time.sleep(self.sleep_length)


if __name__ == '__main__':
    # create and start our threads
    threads = list()
    for i in range(4):
        t = SleepingThread()
        threads.append(t)
        print('Starting Thread {}'.format(i))
        t.start()

    # wait for each to finish (join)
    for i, t in enumerate(threads):
        t.join()
        print('Thread {} Stopped'.format(i))
