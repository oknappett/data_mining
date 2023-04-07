# transfer ship data to a MongoDB collection

# get a connection to MongoDB
import pymongo

user = 'olk11'
dbpath = 'nosql.dcs.aber.ac.uk/olk11'
password = "7LwEV4mUxIqd"
connection_string = 'mongodb://olk11:7LwEV4mUxIqd@nosql.dcs.aber.ac.uk/olk11'

client = pymongo.MongoClient(connection_string)

db = client.olk11

# walk the ship data directory to find the excel files

import os
import get_ships

all_ships = []

ships_dir = 'prac2\ship_data'

for root, dirs, files in os.walk(ships_dir):
    for file in files:
        name, ext = os.path.splitext(file)
        if ext == '.xlsx':
            all_ships += get_ships.get_ships( os.path.join(root, file) )

result = db.olk11Ships.insert_many(all_ships)
print(result)
