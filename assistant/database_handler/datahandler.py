import json
from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB
# client = MongoClient('mongodb://localhost:27017/')
client = MongoClient('mongodb://34.68.34.160:27017/')
db = client['yoga_db_TEST2']  # Replace 'your_database_name' with your actual database name
collection = db['slots_TEST2']  # Replace 'your_collection_name' with your actual collection name

# Load JSON data from file
with open('dummy_data.json') as file:
    data = json.load(file)

# print(data)

# Convert date strings to datetime objects
# for record in data:
#     record['date'] = datetime.strptime(record['date'], '%Y-%m-%d')

# Insert data into MongoDB
collection.insert_many(data)

# Close the MongoDB connection
client.close()
print("SUCCESS!!")
