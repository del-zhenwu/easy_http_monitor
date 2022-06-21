# -*- coding: utf-8 -*-
import time
from datetime import datetime
import logging

logger = logging.getLogger('easy_http.utils.timer')


class Counter(object):

    """The counter class."""

    def __init__(self):
        self.start()

    def start(self):
        self.target = datetime.now()

    def reset(self):
        self.start()

    def get(self):
        return (datetime.now() - self.target).total_seconds()


class Timer(object):

    """The timer class. A simple chronometer."""

    def __init__(self, duration):
        self.duration = duration
        self.start()

    def start(self):
        self.target = time.time() + self.duration

    def reset(self):
        self.start()

    def get(self):
        return self.duration - (self.target - time.time())

    def set(self, duration):
        self.duration = duration

    def finished(self):
        return time.time() > self.target


def get_current_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
