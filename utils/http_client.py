# -*- coding: utf-8 -*-
import json
import logging
import socket
import traceback
import requests
from config import Config

config = Config()
logger = logging.getLogger('easy_http.utils.http_client')


class HttpClient(object):
    """
    Base http-client class for requests
    """
    def __init__(self, domain, headers=None, timeout=None, verify_ssl=None, username=None, password=None):
        self.domain = domain
        self.timeout = timeout
        if headers is None:
            self.headers = {'Content-Type': 'application/json'}
        else:
            self.headers = headers
        self.method_kwargs = {}
        if verify_ssl is not None:
            self.method_kwargs['verify'] = verify_ssl
        if username is not None and password is not None:
            self.method_kwargs['auth'] = (username, password)

    def _http_response(self, url, method, data=None, **kwargs):
        """
        :param url: target url
        :param method: method from requests
        :param data: request body
        :param kwargs: url formatting args
        :return: http response
        """
        response = requests.Response()
        # Prepare call before sending a request
        if not self._prepare_call():
            response.status_code = config.UNKNOWN_SERVER_CODE
            response.reason = "Resolving domain: %s failed" % self.domain
            return response
        try:
            # Sending a request
            path = url.format(**kwargs)
            logger.debug("%s %s" % (method.__name__.upper(), self.domain+path))
            if method.func_name == 'post':
                response = method(self.domain+path,
                                  data=json.dumps(data), headers=self.headers, timeout=self.timeout, **self.method_kwargs)
            elif method.func_name == 'get':
                response = method(self.domain+path,
                                  params=kwargs, headers=self.headers, timeout=self.timeout, **self.method_kwargs)
            elif method.func_name == 'delete':
                response = method(self.domain+path, headers=self.headers, timeout=self.timeout, **self.method_kwargs)
            else:
                logger.error("Method %s not support" % method.func_name)
                return None
            logger.debug("Request result <code: %s, reason: %s>" % (response.status_code, response.reason))

        except Exception as e:
            logger.error("Request failed: %s" % str(e))
            response.reason = str(e)
            # logger.error(traceback.format_exc())
            # if response:
            #     response.raise_for_status()

        finally:
            return response

    def http_call(self, url, method, data=None, **kwargs):
        """
        call _http_response function
        :param url:
        :param method:
        :param data:
        :param kwargs:
        :return:
        """
        return self._http_response(url, method, data=data, **kwargs)

    def _prepare_call(self):
        res = True
        try:
            logger.debug("Start resolving domain <%s>" % self.domain)
            # socket.gethostbyname(self.domain)
            tmp_domain = self.domain
            tmp_port = 80
            if tmp_domain.startswith("http"):
                tmp_domain = tmp_domain.split("http://")[1]
                if tmp_domain.startswith("www"):
                    tmp_domain = tmp_domain.split("www.")[1]
            if tmp_domain.split("/")[0].find(":") != -1:
                tmp_domain = tmp_domain.split("/")[0].split(":")[0] 
                tmp_port = tmp_domain.split("/")[0].split(":")[1]
            logger.debug(tmp_domain)
            logger.debug(tmp_port)
            socket.getaddrinfo(tmp_domain, tmp_port, 0, 0, socket.IPPROTO_TCP) 
        except Exception as e:
            logger.error("Server <%s> not known" % self.domain)
            logger.error(str(e))
            res = False
        finally:
            return res
