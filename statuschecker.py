# -*- coding: utf-8 -*-
"""
An example url status checker implementation that checks 1 URL per thread.
"""

import threading
import requests

class StatusChecker(threading.Thread):
    """
    The thread that will check HTTP statuses.
    """

    #: The url this thread will check
    to_check = None

    #: The status code of the check url
    status_code = None

    def __init__(self, to_check):
        super().__init__()
        self.to_check = to_check

    def run(self):
        resp = requests.get(self.to_check)
        self.status_code = resp.status_code


if __name__ == '__main__':
    urls = (
        'http://httpbin.org/status/418',
        'http://httpbin.org/status/200',
        'http://httpbin.org/status/404',
        'http://httpbin.org/status/500',
    )

    threads = dict()
    for url in urls:
        threads[url] = StatusChecker(url)
        print('Starting check for {}'.format(url))
        threads[url].start()

    for _, thread in threads.items():
        thread.join()

    for url in urls:
        print('{} - {}'.format(url, threads[url].status_code))
