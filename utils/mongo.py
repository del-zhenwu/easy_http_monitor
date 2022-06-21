import sys
import logging
from pymongo import MongoClient, ASCENDING
from bson.objectid import ObjectId
from timer import get_current_time

logger = logging.getLogger('easy_http.utils')


class MongoConn(object):
    def __init__(self, host, port=27017, db_name='', user=None, passwd=None):
        self.collection = None
        try:
            self.conn = MongoClient(host, port)
            if user is None:
                self.db = self.conn[db_name]
            else:
                db_auth = self.conn[db_name]
                db_auth.authenticate(user, passwd)
                self.db = self.conn[db_name]
        except Exception as e:
            raise Exception("Cannot connect to %s:%s, %s" % (host, port, str(e)))

    def table(self, table_name):
        if not self.db:
            logger.error("no db")
            sys.exit(0)
        self.collection = self.db[table_name]
        return self.collection

    def drop_database(self, db_name):
        self.conn.drop_database(db_name)

    def clear_database(self):
        self.db.remove({})


class Collection(object):
    def __init__(self, mongoconn, table):
        self.table = table
        self.collection = mongoconn.table(table)

    @property
    def name(self):
        return self.table

    def new_doc_object(self):
        doc = {
            "_id": str(ObjectId()),
            "ctime": get_current_time()
        }
        return doc

    def find(self, query=None, limit=None, sort=None):
        results = None
        if not self.collection:
            logger.error("no collection")
            return results
        if sort is None:
            if limit:
                results = self.collection.find(query).limit(limit)
            else:
                results = self.collection.find(query)
        else:
            if limit:
                results = self.collection.find(query).sort(sort).limit(limit)
            else:
                results = self.collection.find(query)
        if results:
            return list(results)
        else:
            return None

    def find_one(self, query=None):
        result = self.collection.find_one(query)
        return result

    def exists(self, key):
        res = False
        tmp = self.collection.find_one({'_id': key})
        if tmp is not None:
            res = True
        return res

    def is_empty(self):
        res = self.collection.find_one()
        if res:
            return False
        else:
            return True

    def count(self, query=None):
        count = self.find(query).count()
        return count

    def insert_one(self, dic):
        self.collection.insert_one(dic)

    def insert_many(self, l):
        self.collection.insert(l)

    def remove(self):
        self.collection.drop()

    def delete_one(self, query):
        self.collection.delete_one(query)

    def delete_by_id(self, id):
        query = {'_id': id}
        self.delete_one(query)

    def update_one(self, query, update):
        self.collection.update_one(query, {'$set': update})

    def delete_row(self, query, row):
        self.collection.update_one(query, {'$unset': {row: ""}})

    def update_by_id(self, id, update):
        query = {'_id': id}
        self.update_one(query, update)



