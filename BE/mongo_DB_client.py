from pymongo import MongoClient

class MongoDBClient:
    def __init__(self, uri, database_name):
        self.client = MongoClient(uri)
        self.database = self.client[database_name]

    def insert_many(self, collection_name, documents):
            collection = self.database[collection_name]
            result = collection.insert_many(documents)
            return result.inserted_ids
    
    def insert_one(self, collection_name, document):
        collection = self.database[collection_name]
        result = collection.insert_one(document)
        return result.inserted_id
    
    def find(self, collection_name, query={}):
        collection = self.database[collection_name]
        if query:
            result
        else:
            result = collection.find()
        return list(result)
    
    def find_one(self, collection_name, query):
        collection = self.database[collection_name]
        if query:
            result = collection.find_one(query)
        else:
            result = collection.find_one()
        return result
    
    def update_one(self, collection_name, query, update):
        collection = self.database[collection_name]
        result = collection.update_one(query, update)
        return result.modified_count
    
    def update_many(self, collection_name, query, update):
        collection = self.database[collection_name]
        result = collection.update_many(query, update)
        return result.modified_count
    
    def delete_one(self, collection_name, query):
        collection = self.database[collection_name]
        result = collection.delete_one(query)
        return result.deleted_count
    
    def delete_many(self, collection_name, query):
        collection = self.database[collection_name]
        result = collection.delete_many(query)
        return result.deleted_count
    
    def aggregate(self, collection_name, pipeline):
        collection = self.database[collection_name]
        result = collection.aggregate(pipeline)
        return list(result)
    
    def count(self, collection_name, query={}):
        collection = self.database[collection_name]
        result = collection.count_documents(query)
        return result
    
    def distinct(self, collection_name, field, query={}):
        collection = self.database[collection_name]
        result = collection.distinct(field, query)
        return result
    
    def drop_collection(self, collection_name):
        collection = self.database[collection_name]
        collection.drop()