import pprint

from pymongo import MongoClient
client = MongoClient('mongodb://olk11:7LwEV4mUxIqd@nosql.dcs.aber.ac.uk/olk11')

db = client.olk11

cursor = db.olk11.aggregate([{
    "$match": {"vessel name": "Loyalty"}
}, {"$project": {
    "_id": 0,
    "vessel name": "$vessel name",
    "mariners": "$mariners"
}}])

for doc in cursor:
    pprint.pprint(doc)