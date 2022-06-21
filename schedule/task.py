# -*- coding: utf-8 -*-
import logging
from alert import alert
from agent import collect

logger = logging.getLogger('easy_http.schedule.task')


def task_runner(scanner_or_server, http_config):
    if scanner_or_server == "alerter":
        alert.do_alert(http_config)
    elif scanner_or_server == "scanner":
        collect.collect_http_stats(http_config)

