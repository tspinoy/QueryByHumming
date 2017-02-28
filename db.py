from pymongo import MongoClient

client = MongoClient('localhost', 8080)

db = client.test_database

test = db.dataset
print db
print test