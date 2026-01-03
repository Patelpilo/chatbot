from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"

client = MongoClient(MONGO_URI)

print("CONNECTED DATABASES:", client.list_database_names())

db = client["whatsease"]

users_collection = db["users"]
messages_collection = db["messages"]
