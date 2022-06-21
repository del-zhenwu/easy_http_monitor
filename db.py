import logging
import redis
from bson.objectid import ObjectId
from utils.mongo import MongoConn, Collection
from utils import timer
from config import Config

logger = logging.getLogger('easy_http.db')

config = Config()
mdb = MongoConn(config.MONGODB_HOST, db_name=config.MONGODB_NAME)


class CoConfig(Collection):
    def __init__(self):
        super(CoConfig, self).__init__(mdb, "co_config")

    def get(self, config_id):
        return self.find_one(query={"_id": config_id})

    def get_all(self):
        return list(self.find(query={"state": 1}))

    def get_groups(self):
        groups = []
        configs = self.get_all()
        for config_item in configs: 
            if "group" in config_item and config_item["group"] not in groups:
                groups.append(config_item["group"])
        return groups

    def juhe(self):
        res = {}
        configs = self.get_all()
        for config_item in configs:
            group = str(config_item["group"])
            app_name = str(config_item["app_name"])
            if group in res:
                if app_name in res[group]:
                    res[group][app_name].append(config_item)
                else:
                    res[group].update({app_name: [config_item]})
            else:
                res[group] = {app_name: []}
                res[group][app_name].append(config_item)
        return res

    def update(self, config_id, data):
        pass


class CoDetail(Collection):
    def __init__(self):
        super(CoDetail, self).__init__(mdb, "co_detail")

    def add(self, doc):
        self.insert_one(doc)

    def init_doc(self, http_config):
        detail_doc = {
            "config_id": http_config["_id"],
            "app_name": http_config["app_name"],
            "domain": http_config["domain"],
            "url": http_config["url"],
            "content": {},
            "c_time": timer.get_current_time()
        }
        return detail_doc


class CoScanner(Collection):
    def __init__(self):
        super(CoScanner, self).__init__(mdb, "scanner_job")


class CoAlerter(Collection):
    def __init__(self):
        super(CoAlerter, self).__init__(mdb, "alerter_job")
