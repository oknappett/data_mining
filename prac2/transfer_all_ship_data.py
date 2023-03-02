# transfer ship data to a MongoDB collection

# get a connection to MongoDB
import pymongo

user = 'olk11'
dbpath = 'nosql.dcs.aber.ac.uk/olk11'
password = "7LwEV4mUxIqd"
connection_string = 'mongodb://'+user+':'+password+'@'+dbpath

client = pymongo.MongoClient(connection_string)

db = client.olk11

# walk the ship data directory to find the excel files

import os
import get_ships

all_ships = []

ships_dir = '/aber/olk11/data_mining/prac2/ship_data/ABERSHIP_transcription_vtls004566921'

for root, dirs, files in os.walk(ships_dir):
    for file in files:
        name, ext = os.path.splitext(file)
        if ext == '.xlsx':
            all_ships += get_ships.get_ships( os.path.join(root, file) )

result = db.olk11.insert_many(all_ships)
print(result)
