# -*- coding: utf-8 -*-
import logging
import json
import traceback
from flask import request
from flask import Blueprint
from db import CoConfig

logger = logging.getLogger('easy_http.api.views')
mod = Blueprint('api', __name__, url_prefix='/api')


def handler_core(data):
    res = {"msg": "", "code": 200, "data": {}}
    try:
        if "ip" not in data:
            res["code"] = 400
            res["msg"] = "no ip in params"
        else:
            ip = data["ip"]
            CoConfig().update_machine(ip)
            if "app" in data:
                app_info = data["app"]
                CoConfig().update_app(ip, app_info)
    except Exception as e:
        logger.error(traceback.format_exc())
        logger.debug(str(e))
        res["code"] = 500
        res["msg"] = str(e)
    return json.dumps(res)


@mod.route("/app/handler", methods=['POST'])
def app_handler():
    logger.error(request.data)
    return handler_core(json.loads(request.data))


@mod.route("/host/delete/<ip>", methods=['GET'])
def host_delete(ip):
    res = {"msg": "", "code": 200, "data": {}}
    try:
        CoConfig().delete_by_id(ip)
    except Exception as e:
        logger.error(traceback.format_exc())
        logger.debug(str(e))
        res["code"] = 500
        res["msg"] = str(e)
    return json.dumps(res)
