from pymongo import MongoClient

class MongoDBHandler:
    def __init__(self, database_name =None, collection_name=None):
        # self.client = MongoClient('mongodb://34.68.34.160:27017/')
        self.client = MongoClient('mongodb://localhost:27017/')
        self.database_name = database_name or 'default_database'
        self.collection_name = collection_name or 'default_collection'
        self.db = self.client[self.database_name]
        self.collection = self.db[self.collection_name]

    def create_collection(self, collection_name):
        self.collection = self.db[collection_name]

    def insert_data(self, data, insert_many = False):
        if insert_many:
            result = self.collection.insert_many(data)
        else:
            result = self.collection.insert_one(data)
            print(f"Inserted document with ID: {result.inserted_id}")

    def fetch_data(self, query=None):
        if query is None:
            cursor = self.collection.find()
        else:
            cursor = self.collection.find(query)

        result = [document for document in cursor]
        return result

    def delete_data(self, query):
        result = self.collection.delete_one(query)
        print(f"Deleted {result.deleted_count} document(s)")

    def update_data(self, query, new_values):
        result = self.collection.update_one(query, {'$set': new_values})
        print(f"Updated {result.modified_count} document(s)")

    def drop_collection(self):
        self.collection.drop()
        print(f"Collection {self.collection.name} dropped.")

    def close_connection(self):
        self.client.close()

    def get_result(self, query,keys=None):
        print("in Mongodb query")
        result = self.collection.find(query,keys)
        return result
    


def connect_to_database(client_url):
    client = MongoClient(client_url)
    db = client.yoga_db
    collections = {
        "slots_collection": db.slots,
        # "learn_and_grow_collection": db.learn_and_grow,
        # "feedback_collection" : db.feedback
    }
    return collections

def get_collections():
    collections = connect_to_database()
    slots_collection = collections["slots_collection"]
    # learn_and_grow_collection = collections["learn_and_grow_collection"]
    # feedback_collection = collections["feedback_collection"]
    print("yeee MongoDB connected successfully!!")
    return slots_collection#, learn_and_grow_collection, feedback_collection
