# -*- coding: utf-8 -*-
"""
An example url status checker implementation consumes urls from a queue.
"""

import threading
import queue
import requests

class StatusChecker(threading.Thread):
    """
    The thread that will check HTTP statuses.
    """

    #: The queue of urls
    url_queue = None

    #: The queue our results will go into
    result_queue = None

    def __init__(self, url_queue, result_queue):
        super().__init__()
        self.url_queue = url_queue
        self.result_queue = result_queue

    def run(self):
        while True:
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


if __name__ == '__main__':
    urls = (
        'http://httpbin.org/status/418',
        'http://httpbin.org/status/200',
        'http://httpbin.org/status/404',
        'http://httpbin.org/status/500',
    )

    url_queue = queue.Queue()
    for url in urls:
        url_queue.put(url)

    result_queue = queue.Queue()
    num_workers = 2
    for i in range(num_workers):
        t = StatusChecker(url_queue, result_queue)
        print('Starting worker {}'.format(i))
        t.start()

    # wait for the queue to empty
    url_queue.join()

    while not result_queue.empty():
        url, status = result_queue.get_nowait()
        print('{} - {}'.format(url, status))
