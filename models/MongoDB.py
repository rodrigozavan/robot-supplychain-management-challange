from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId
from config import config

HOST = config.get('MONGODB', 'host')
DATABASE = config.get('MONGODB', 'database')

class MongoDB:
    def __init__(self, collection_name):
        self.db = Model()
        self.collection_name = collection_name

    def create(self, data):
        res = self.db.insert(data, self.collection_name)
        return res

    def find(self, data, sort=None):
        return self.db.find(data, self.collection_name, None, sort)

    def find_by_id(self, _id):
        return self.db.find_by_id(_id, self.collection_name)

    def update_one(self, _id, data):
        return self.db.update_one(_id, data, self.collection_name)

    def update_many(self, _id, data):
        return self.db.update_many(_id, data, self.collection_name)

    def upsert(self, _id, user):
        return self.db.upsert(_id, user, self.collection_name)

    def push(self, criteria, upd):
        return self.db.push(criteria, upd, self.collection_name)

    def delete_one(self, _id):
        return self.db.delete_one(_id, self.collection_name)

    def delete_many(self, _id):
        return self.db.delete_many(_id, self.collection_name)

    def count(self):
        return self.db.count(self.collection_name)


class Model:
    def __init__(self):
        self.client = MongoClient(HOST)
        self.db = self.client[DATABASE]

    def insert(self, element, collection_name):
        element["created_at"] = datetime.now()
        element["updated_at"] = datetime.now()

        inserted = self.db[collection_name].insert_one(element)
        return str(inserted.inserted_id)

    def find(self, criteria, collection_name, projection=None, sort=None, limit=0, cursor=False):

        if "_id" in criteria:
            criteria["_id"] = ObjectId(criteria["_id"])

        found = self.db[collection_name].find(filter=criteria, projection=projection, limit=limit, sort=sort)

        if cursor:
            return found

        found = list(found)

        for i in range(len(found)):
            if "_id" in found[i]:
                found[i]["_id"] = str(found[i]["_id"])

        return found

    def find_by_id(self, _id, collection_name):
        found = self.db[collection_name].find_one({"_id": ObjectId(_id)})

        if found is None:
            return not found

        if "_id" in found:
            found["_id"] = str(found["_id"])

        return found

    def update_one(self, criteria, element, collection_name):
        if "_id" in criteria:
            criteria["_id"] = ObjectId(criteria["_id"])
        element["updated_at"] = datetime.now()
        set_obj = {"$set": element}
        updated = self.db[collection_name].update_one(criteria, set_obj)
        if updated.matched_count == 1:
            return "Record Successfully Updated"

    def update_many(self, criteria, element, collection_name):
        if "_id" in criteria:
            criteria["_id"] = ObjectId(criteria["_id"])
        element["updated_at"] = datetime.now()
        set_obj = {"$set": element}
        updated = self.db[collection_name].update_many(criteria, set_obj)
        if updated.matched_count == 1:
            return "Record Successfully Updated"

    def upsert(self, criteria, element, collection_name):
        if "_id" in criteria:
            criteria["_id"] = ObjectId(criteria["_id"])
        element["updated_at"] = datetime.now()
        set_obj = {"$set": element}

        updated = self.db[collection_name].update_one(criteria, set_obj, upsert=True)
        if updated.matched_count == 1:
            return "Record Successfully Updated/Inserted"

    def push(self, criteria, element, collection_name):
        if "_id" in criteria:
            criteria["_id"] = ObjectId(criteria["_id"])
        set_obj = {"$push": element}
        updated = self.db[collection_name].update_one(criteria, set_obj)
        if updated.matched_count == 1:
            return "Record Successfully Updated"

    def pull(self, criteria, element, collection_name):
        if "_id" in criteria:
            criteria["_id"] = ObjectId(criteria["_id"])
        set_obj = {"$pull": element}
        updated = self.db[collection_name].update_one(criteria, set_obj)
        if updated.matched_count == 1:
            return "Record Successfully Updated"

    def delete_one(self, _id, collection_name):
        deleted = self.db[collection_name].delete_one({"_id": ObjectId(_id)})
        return bool(deleted.deleted_count)

    def delete_many(self, criteria, collection_name):
        if "_id" in criteria:
            criteria["_id"] = ObjectId(criteria["_id"])
        deleted = self.db[collection_name].delete_many(criteria)
        return bool(deleted.deleted_count)

    def count(self, collection_name):
        countd = self.db[collection_name].count()
        return countd

    def unset(self, criteria, element, collection_name):
        if "_id" in criteria:
            criteria["_id"] = ObjectId(criteria["_id"])
        element["updated_at"] = datetime.now()
        set_obj = {"$unset": element}
        updated = self.db[collection_name].update_one(criteria, set_obj)
        if updated.matched_count == 1:
            return "Record Successfully Updated"