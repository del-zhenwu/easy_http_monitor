# -*- coding: utf-8 -*-
import json
import time
import logging
import traceback
import threading
from requests import get, post
from utils.http_client import HttpClient

logger = logging.getLogger('easy_http.agent.http')


class HttpPlugin(threading.Thread):
    def __init__(self, stats, callback=None, callback_args=None):
        """
        :param stats: {domain, url, method, headers, params, assert, timeout}
        :param callback:
        :param callback_args:
        """
        # logger.debug("ports plugin - Create thread for scan list {}".format(stats))
        super(HttpPlugin, self).__init__()
        # Event needed to stop properly the thread
        self._stopper = threading.Event()
        # The class return the stats as dict
        self._stats = stats
        self.callback = callback
        self.callback_args = callback_args
        # Is part of Ports plugin
        self.plugin_name = "http"

    def run(self):
        """Function called to grab stats.
        Infinite loop, should be stopped by calling the stop() method"""
        # End of the thread has been asked
        if self.stopped():
            return
        # Scan an URL
        self._http_scan()
        # stat = self._http_scan()
        # self.stats(stat)
        # Had to wait between two scans
        # If not, result are not ok
        time.sleep(0.01)
        if self.callback is not None:
            self.callback(**self.callback_args)

    @property
    def stats(self):
        """Stats getter"""
        return self._stats

    @stats.setter
    def stats(self, value):
        """Stats setter"""
        self._stats = value

    def stop(self):
        """Stop the thread"""
        # logger.debug("ports plugin - Close thread for scan list {}".format(self._stats))
        self._stopper.set()

    def stopped(self):
        """Return True is the thread is stopped"""
        return self._stopper.isSet()

    def _http_scan(self):
        """Scan the web-api and update the stat key"""
        try:
            domain = self._stats["domain"]
            url = self._stats["url"]
            if "timeout" in self._stats:
                timeout = self._stats["timeout"]
            else:
                timeout = 2
            if "headers" in self._stats and self._stats["headers"]:
                cli = HttpClient(domain, headers=self._stats["headers"], timeout=timeout)
            else:
                cli = HttpClient(domain, timeout=timeout)
            method_str = self._stats["method"].lower()
            data = self._stats["data"]
            if method_str == "post":
                method = post
                response = cli.http_call(url, method, data=data)
            elif method_str == "get":
                method = get
                response = cli.http_call(url, method, **data)
            else:
                msg = "Method <%s> not supported" % method_str
                logger.error(msg)
                self._stats["code"] = -1
                self._stats["msg"] = msg
                return self._stats
            logger.debug("Url: %s, status_code: %s, key: %s" % (url, response.status_code, self._stats["_id"]))
            logger.debug("Url: %s" % response.url)
            if not response:
                msg = "Http response is empty"
                self._stats["code"] = -2
                self._stats["msg"] = msg
                return self._stats
            self._stats["code"] = response.status_code
            self._stats["msg"] = response.reason
            if response.content:
                try:
                    self._stats["content"] = json.loads(response.content)
                except Exception as e:
                    if response.content.startswith("<!DOCTYPE html>"):
                        logger.debug("HTML response")
                        self._stats["content"] = "html" 
                    else:
                        self._stats["content"] = {}
            else:
                self._stats["content"] = {}
        except Exception as e:
            logger.error("{}: Error while scanning api {} ({})".format(self.plugin_name, url, e))
            logger.error(traceback.format_exc())
            self._stats["code"] = -3
            self._stats["msg"] = str(e)
        finally:
            return self._stats
