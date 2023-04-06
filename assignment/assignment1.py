from pymongo import MongoClient
import pprint
import matplotlib.pyplot as plt

#Mongodb user details for olk11
mongoUser = 'olk11'
mongoPass = '7LwEV4mUxIqd'
client = MongoClient(f'mongodb://{mongoUser}:{mongoPass}@nosql.dcs.aber.ac.uk/olk11')
db = client.olk11

def count_record():
    #the shipping record data is imported into a collection called olk11ShipsData
    cursor = db.olk11ShipsData.find()
    count = len(cursor)

    print("Number of shipping records: ", count)

def vessel_barchart():
    ships = db.olk11ShipsData.aggregate([
                                            {
                                                "$group": 
                                                {"_id": "$vessel name", "count":{"$sum": 1}},
                                            },
                                            {
                                                "$match":   
                                                {"count": {"$gte": 80}}
                                            }])   
    ship_count = {}
    for ship in ships:
        ship_count[ship['_id']] = ship['count']
    ship_names = list(ship_count.keys())
    ship_nums = list(ship_count.values())
    
    plt.bar(range(len(ship_count)), ship_nums, tick_label=ship_names)
    plt.xticks(rotation=45)
    plt.show()

if __name__ =='__main__':
    vessel_barchart()