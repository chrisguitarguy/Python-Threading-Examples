# -*- coding: utf-8 -*-
"""
A simple threading example. Create some threads by passing in a callable to the
`threading.Thread` constructor, keep track of them and wait for them to join.
"""

import random
import threading
import time

def sleeper():
    time.sleep(random.randrange(1, 20))

if __name__ == '__main__':
    # create and start our threads
    threads = list()
    for i in range(4):
        t = threading.Thread(target=sleeper) # pass in the callable
        threads.append(t)
        print('Starting Thread {}'.format(i))
        t.start()

    # wait for each to finish (join)
    for i, t in enumerate(threads):
        t.join()
        print('Thread {} Stopped'.format(i))
