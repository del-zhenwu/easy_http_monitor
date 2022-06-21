# -*- coding: utf-8 -*-
import traceback
import logging
from db import CoDetail
from http import HttpPlugin
from utils.decorator import time_wrapper

logger = logging.getLogger('easy_http.agent.collect')


@time_wrapper
def collect_http_stats(http_config):
    """
    :param http_config:监控项HTTP配置信息：
        {app_name, domain, url, method, headers, params, asserts, timeout}
    :return: res: Boolean
    """
    res = True
    try:
        mp = HttpPlugin(http_config)
        mp.start()
        mp.join()
        mp.stop()
        stat_item = mp.stats
        detail = CoDetail()
        doc = detail.init_doc(http_config)
        doc["code"] = stat_item["code"]
        doc["msg"] = stat_item["msg"]
        doc["content"] = stat_item["content"]
        detail.add(doc)
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        res = False
    finally:
        return res


if __name__ == "__main__":
    collect_http_stats()
