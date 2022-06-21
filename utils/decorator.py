# -*- coding: utf-8 -*-
import time
import traceback
import logging

logger = logging.getLogger('easy_http.utils.decorator')


def views_wrapper(func):
    def wrapper(*args, **kwargs):
        res = {'code': 0, 'msg': '', 'data': {}}
        try:
            res['data'] = func(*args, **kwargs)
        except Exception as e:
            logger.error(str(e))
            logger.error(traceback.format_exe())
            res['code'] = 500
            res['msg'] = str(e)
        return res
    return wrapper


def time_wrapper(func):
    def wrapper(*args, **kwargs):
        tb = time.time()
        func(*args, **kwargs)
        te = time.time()
        logger.info("Spend time: %s" % (te - tb))
    return wrapper
