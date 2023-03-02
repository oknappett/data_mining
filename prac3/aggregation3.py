import pprint

from pymongo import MongoClient
client = MongoClient('mongodb://olk11:7LwEV4mUxIqd@nosql.dcs.aber.ac.uk/olk11')

db = client.olk11

outputfile = open("mariners_ships", encoding="utf-8", mode="w")

cursor = db.olk11.aggregate([
     {"$unwind": "$mariners"},
     {"$group": {"_id": "$mariners.name", 
                "ships": {"$push": {"vessel name": "$vessel name",
                        "capacity": "$mariners.this_ship_capacity",
                        "age": "$mariners.age",
                        "date": "$mariners.this_ship_joining_date"}}}}
])

for doc in cursor:
    pprint.pprint(doc, outputfile)