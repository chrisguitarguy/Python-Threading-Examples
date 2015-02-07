# -*- coding: utf-8 -*-
"""
An example url status checker that uses events to stop threads.
"""

import threading
import queue
import signal
import sys
import requests

class StatusChecker(threading.Thread):
    """
    The thread that will check HTTP statuses.
    """

    #: The queue of urls
    url_queue = None

    #: The queue our results will go into
    result_queue = None

    #: An event that tells the thread to stop
    stopper = None

    def __init__(self, url_queue, result_queue, stopper):
        super().__init__()
        self.url_queue = url_queue
        self.result_queue = result_queue
        self.stopper = stopper

    def run(self):
        while not self.stopper.is_set():
            try:
                # this will throw queue.Empty immediately if there's
                # no tasks left
                to_check = self.url_queue.get_nowait()
            except queue.Empty:
                break # empty queue, we're done!
            else:
                resp = requests.get(to_check)
                self.result_queue.put((to_check, resp.status_code,))
                self.url_queue.task_done() # the the queue we're done


class SignalHandler:
    """
    The object that will handle signals and stop the worker threads.
    """

    #: The stop event that's shared by this handler and threads.
    stopper = None

    #: The pool of worker threads
    workers = None

    def __init__(self, stopper, workers):
        self.stopper = stopper
        self.workers = workers

    def __call__(self, signum, frame):
        """
        This will be called by the python signal module

        https://docs.python.org/3/library/signal.html#signal.signal
        """
        self.stopper.set()

        for worker in self.workers:
            worker.join()

        sys.exit(0)


if __name__ == '__main__':
    # all the variables we'll need
    num_workers = 2
    stopper = threading.Event()
    result_queue = queue.Queue()
    url_queue = queue.Queue()

    # populate our work queue
    for i in range(100):
        url_queue.put('http://httpbin.org/status/418')

    # we need to keep track of the workers but not start them yet
    workers = [StatusChecker(url_queue, result_queue, stopper) for i in range(num_workers)]

    # create our signal handler and connect it
    handler = SignalHandler(stopper, workers)
    signal.signal(signal.SIGINT, handler)

    # start the threads!
    for i, worker in enumerate(workers):
        print('Starting worker {}'.format(i))
        worker.start()

    # wait for the queue to empty
    url_queue.join()

    while not result_queue.empty():
        url, status = result_queue.get_nowait()
        print('{} - {}'.format(url, status))
