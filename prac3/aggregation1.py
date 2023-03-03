# a first aggregation pipeline with just one $match operation

import pprint

from pymongo import MongoClient
client = MongoClient('mongodb://olk11:7LwEV4mUxIqd@nosql.dcs.aber.ac.uk/olk11')

db = client.olk11

cursor = db.olk11.aggregate([{"$match": {
    "vessel name": "Loyalty"
}}, {"$project": {
    "vessel name": 1,
    "_id": 0,
    "count_mariners": {"$size": "$mariners"}
}}])

for doc in cursor:
    pprint.pprint(doc)