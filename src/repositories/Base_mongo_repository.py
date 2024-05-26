from bson.objectid import ObjectId

from src.enums.Update_type import UpdateType


class BaseRepository:
    def __init__(self, collection):
        self.collection = collection

    def find_by_id(self, id):
        return self.collection.find_one({"_id": ObjectId(id)})

    def find_all(self, filter=None):
        filter = filter or {}
        return self.collection.find(filter)

    def insert_one(self, document):
        return self.collection.insert_one(document)

    def update_one(self, filter, update, update_type=UpdateType.UPDATE_ONLY_VALUES):
        if update_type == UpdateType.UPDATE_ONLY_VALUES:
            return self.collection.update_one(filter, {"$set": update})
        elif update_type == UpdateType.UPDATE_VALUES:
            existing_document = self.collection.find_one(filter)
            if not existing_document:
                return None
            for key, value in update.items():
                existing_document[key] = value
            return self.collection.replace_one(filter, existing_document)
        elif update_type == UpdateType.UPDATE_AND_NULL_ALL:
            existing_document = self.collection.find_one(filter)
            if not existing_document:
                return None
            for key in existing_document.keys():
                if key not in update:
                    update[key] = None
            return self.collection.replace_one(filter, update)
        else:
            raise ValueError("Invalid update type specified")

    def delete_one(self, filter):
        return self.collection.delete_one(filter)

    def find_one(self, filter):
        return self.collection.find_one(filter)

    def update_by_id(self, id, update, update_type=UpdateType.UPDATE_ONLY_VALUES):
        return self.update_one({"_id": ObjectId(id)}, update, update_type)

    def delete_by_id(self, id):
        return self.collection.delete_one({"_id": ObjectId(id)})
