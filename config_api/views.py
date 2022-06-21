# -*- coding: utf-8 -*-
import logging
import traceback
import json
from flask import Blueprint, current_app as app 
from flask import request, render_template, jsonify
from config_api import APIMixin, set_receivers
from db import CoConfig, CoScanner, CoAlerter
from schedule.schedule import SchedulerWrapper

logger = logging.getLogger('easy_http.config_api.views')
mod = Blueprint('/config', __name__, url_prefix='/config')


@mod.route("/", methods=['GET'])
def index():
    configs = []
    try:
        configs = CoConfig().juhe()
    except Exception as e:
        logger.debug(str(e))
        logger.error(traceback.format_exc())
    if 'type' in request.args and request.args['type'] == 'json':
        return jsonify(configs)
    else:
        return render_template('dashboard.html', res=configs)


@mod.route("/info/<config_id>", methods=['GET'])
def config_info(config_id):
    config_item = CoConfig().find_one({"_id": config_id})
    if 'type' in request.args and request.args['type'] == 'json':
        return jsonify(config_item)
    else:
        return render_template('info.html', res=config_item)


@mod.route("/remove", methods=['GET'])
def config_invalid():
    res = APIMixin().api_res
    if "config_id" in request.args and request.args["config_id"]:
        config_id = request.args["config_id"]
    else:
        res["code"] = 400
        res["msg"] = "config_id有误"
        return json.dumps(res) 
    try:
        config_item = CoConfig().find_one({"_id": config_id})
        CoConfig().update_by_id(config_id, {"state": 0})
        CoScanner().delete_by_id(config_id)
        CoAlerter().delete_by_id(config_id)
        res["msg"] = "操作成功"
    except Exception as e:
        res["code"] = 500
        res["msg"] = "操作失败：%s" % str(e)
        logger.error(res["msg"])
    finally:
        return json.dumps(res) 


@mod.route("/add", methods=['GET'])
def config_add_get():
    groups = CoConfig().get_groups()
    return render_template('add.html', groups=groups)


@mod.route("/set/receivers", methods=['GET'])
def config_set_receivers():
    res = APIMixin().api_res
    configs = CoConfig().get_all()
    for config in configs:
        receivers = set_receivers(config["group"])
        data = {
            "receivers": receivers,
            "assertions": []
        }
        if config["group"] == "c_api":
            data["assertions"] = [{
                "assert_key" : "status",
                "assert_comparison" : "1",
                "assert_value" : 0
            }]
        logger.debug(data)
        CoConfig().update_by_id(config["_id"], data)
    return json.dumps(res)


@mod.route("/add", methods=['POST'])
def config_add():
    res = APIMixin().api_res
    try:
        group = str(request.form.get("group")) 
        app_name = str(request.form.get("app_name"))
        desc = str(request.form.get("desc"))
        domain = str(request.form.get("domain"))
        url = str(request.form.get("url"))
        method = str(request.form.get("method"))
        content_type = str(request.form.get("content_type"))
    except Exception as e:
        msg = "参数缺失或者不合法"
        res["msg"] = msg
        res["code"] = 400
        return json.dumps(res)
    content_type = "application/"+content_type
    if method != "GET" and method != "POST":
        logger.error(method)
        logger.error(type(method))
        msg = "仅支持GET/POST请求"
        res["msg"] = msg
        res["code"] = 400
        return json.dumps(res)
    seconds = request.form.get("seconds", default=app.config["DEFAULT_SCANNER_SECONDS"]) 
    data = request.form.get("parameters", default={})
    assertions = request.form.get("assertions", default=[])
    receivers = set_receivers(group) 
    try:
        if data:
            data = json.loads(data)
            logger.debug(data)
        if assertions:
            assertions = json.loads(assertions)
            logger.debug(assertions)
    except Exception as e:
        msg = "Json loads failed: <%s>" % data
        logger.error(msg)
        res["code"] = 400
        return json.dumps(res)        
    doc = CoConfig().new_doc_object() 
    doc.update({
        "app_name": app_name,
        "group": group,
        "desc": desc,
        "content_type": content_type,
        "domain": domain,
        "url": url,
        "method": method,
        "data": data,
        "auth": {},
        "assertions": assertions,
        "scripts": [],
        "before_scripts": [],
        "seconds": int(seconds),
        "receivers": receivers,
        "state": 1
    })
    try:
        logger.debug(doc)
        CoConfig().insert_one(doc)
        res["msg"] = "新增api成功"
        sw = SchedulerWrapper("scanner")
        sw.start()
        job_ins = sw.add_job(seconds=int(seconds), job_id=doc["_id"], http_config=doc)
        logger.debug("Job<%s>: %s added" % (job_ins, doc["_id"]))
        logger.debug(sw.print_jobs())
    except Exception as e:
        msg = "新增api<domain: %s, url: %s>失败，原因：<%s>" % (domain, url, str(e))
        logger.error(msg)
        res["msg"] = msg
        res["code"] = 500
    return json.dumps(res)


@mod.route("/update/<config_id>", methods=['POST'])
def config_update(config_id):
    res = APIMixin().api_res
    if not CoConfig().exists(config_id):
        msg = "Config id <%s> not existed" % config_id
        res["msg"] = msg
        res["code"] = 400
        return json.dumps(res)
    config_item = CoConfig().get(config_id)
    try:
        request_data = json.loads(request.data)
        logger.debug(request_data)
    except Exception as e:
        msg = "Json loads failed: <%s>" % request.request_data
        logger.error(msg)
        res["code"] = 400
        return json.dumps(res)
    if not CoConfig().update(config_id, data):
        msg = "Update config <%s> failed" % config_id
        res["msg"] = msg
        res["code"] = 500
        return json.dumps(res)

    new_config_item = CoConfig().get(config_id)
    new_seconds = config_item["seconds"]
    if "seconds" in request_data:
        new_seconds = request_data["seconds"]
    # modify scheduler job
    sw = SchedulerWrapper("scanner")
    # sw.start()
    job_ins = sw.modify_job(
        job_id=config_id,
        seconds=new_seconds,
        http_config=new_config_item
    )
    logger.info("Modify job <%s> success" % config_id)
    return json.dumps(res)
