from pymongo import MongoClient
import pprint
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class Mariner:
    def __init__(self, rank='missing', age='missing', name='missing', PlaceOfBirth='missing'):
        self.rank = rank
        self.age = age
        self.name = name
        self.PlaceofBirth = PlaceOfBirth

    def __eq__(self, other):
        return self.rank == other.rank and self.age == other.age and self.name == other.name and self.PlaceofBirth == other.PlaceofBirth

    def setAge(self, age):
        self.age = age

    def setRank(self, rank):
        self.rank = rank

    def setName(self, name):
        self.name = name

    def setPlaceofBirth(self, PoB):
        self.PlaceofBirth = PoB

    def toString(self):
        return f"Name:{self.name} Age:{self.age} Rank:{self.rank} Born:{self.PlaceofBirth}"


# Mongodb user details for olk11
mongoUser = 'olk11'
mongoPass = '7LwEV4mUxIqd'
client = MongoClient(
    f'mongodb://{mongoUser}:{mongoPass}@nosql.dcs.aber.ac.uk/{mongoUser}')
db = client.olk11


def initialPlots():
    '''
    Initial plots of the data before cleaning/handling noise in data
    Used for visualisation and explanation of how the data is handled later
    '''
    # ===part 1:individual stories===
    # plot histogram of ages
    # plot rank distribution
    # plot age at each rank
    # ===part 2:who is visiting===
    # plot ship data
    # plot length of service of crew -> date between joining and leaving
    # plot number of ship visits to each port that inst aberystwyth


def clean_rank(rank):
    '''
    Function to clean ranks. Groups ranks together to eliminate messy data such as spelling
    '''
    # output of ranks, needs to be analysed and changed:
    # dict_keys(['', 'boatswainmaster', 'runner', 'boy', 'stmate', 'master', 'stengineer', 'seaman', 'masterc', 'onlymate',
    # 'cape', 'mate', 'cooksteward', 'ndmate', 'cookandableseaman', 'mastervolunteerscertificatec', 'boatswain', 'ordinaryseaman',
    # 'mateableseaman', 'thengineer', 'botswain', 'purser', 'apprentice', 'bosun', 'skipper', 'secondengineer', 'shipkeeper',
    # 'stoker', 'ableseaman', 'messroomsteward', 'engineersteward', 'bswain', 'ndhand', 'ordinaryseamancook', 'donkeyman', 'cook',
    # 'cookordinaryseaman', 'cookstewardandseaman', 'rdmate', 'pantryboy', 'fireman', 'mater', 'rdhand', 'steward', 'cookstewardseaman',
    # 'captainmaster', 'captain', 'ndengineer', 'bargeman', 'rdengineer', 'crengineer', 'cookableseaman', 'carpenterseaman', 'blk', 'cookseaman',
    # 'cookandsteward', 'bosunandlamps', 'radioofficer', 'lamptrimmer', 'masterowner', 'boson', 'assistantengineer', 'stewardcook', 'helmsman', 'carpenterableseaman',
    # 'mstr', 'donkeyengineoperator', 'matecc', 'mateboatswain', 'cookboy', 'pantrymanfireman', 'stwck', 'firstmate', 'engineer', 'nil', 'ableseamancook', 'ab', 'matepurser',
    # 'sl', 'seman', 'ordinary', 'carpenter', 'secondmate', 'boyordinary', 'enigneer', 'mastershipkeeper', 'messroom', 'cabinboy', 'leadingseaman', 'mastercaptain'])

    # change rank to single string with only alpha characters
    rank = ''.join(c for c in str(rank) if c.isalpha()).lower()

    # change rank to grouped rank
    match rank:
        case captain if captain in ['skipper', 'captainmaster', 'captain', 'mastercaptain']:
            cleaned = 'captain'
        case purser if purser in ['purser', 'matepurser']:
            cleaned = 'purser'
        case master if master in ['master', 'masterc', 'mater', 'captainmaster', 'mstr', 'mastershipkeeper',
                                  'mastercaptain', 'mastervolunteerscertificatec']:
            cleaned = 'master'
        case boatswain if boatswain in ['boatswainmaster', 'boatswain', 'botswain', 'bswain', 'mateboatswain']:
            cleaned = 'boatswain'
        case steward if steward in ['cooksteward', 'messroomsteward', 'engineersteward', 'cookstewardandseaman', 'steward',
                                    'cookstewardseaman', 'cookandsteward', 'stewardcook', 'stwck']:
            cleaned = 'steward'
        case cook if cook in ['cooksteward', 'ordinaryseamancook', 'cook', 'cookordinaryseaman',
                              'cookstewardandseaman', 'cookstewardseaman', 'cookableseaman',
                              'cookseaman', 'cookandsteward', 'stewardcook',  'cookboy', 'ableseamancook']:
            cleaned = 'cook'
        case carpenter if carpenter in ['carpenterseaman', 'carpenterableseaman', 'carpenter']:
            cleaned = 'carpenter'
        case mate if mate in ['onlymate', 'mate', 'ndmate', 'mateableseaman', 'rdmate', 'matecc', 'firstmate',
                              'matepurser', 'secondmate', 'stmate']:
            cleaned = 'mate'
        case able if able in ['cookandableseaman', 'mateableseaman', 'ableseaman', 'cookableseaman', 'carpenterableseaman',
                              'ableseamancook']:
            cleaned = 'able seaman'
        # seaman = ordinary seaman according to me
        case ordinary if ordinary in ['seaman', 'ordinaryseaman', 'ordinaryseamancook', 'cookordinaryseaman', 'cookstewardandseaman',
                                      'cookstewardseaman', 'cookseaman', 'seman', 'ordinary']:
            cleaned = 'ordinary seaman'
        case boy if boy in ['boy', 'pantryboy', 'cookboy', 'boyordinary', 'cabinboy']:
            cleaned = 'boy'
        case engineer if engineer in ['stengineer', 'thengineer', 'secondengineer', 'engineersteward', 'ndengineer',
                                      'rdengineer', 'crengineer', 'assistantengineer', 'engineer', 'enigneer']:
            cleaned = 'engineer'
        case fireman if fireman in ['fireman', 'pantrymanfireman']:
            cleaned = 'fireman'
        case bosun if bosun in ['bosun', 'bosunandlamps', 'lamptrimmer', 'boson']:
            cleaned = 'bosun'
        case hand if 'hand' in rank:
            cleaned = 'hand'
        case _:
            cleaned = 'other'

    return cleaned


def calculate_age(birthYear, leaveYear):
    if (str(birthYear).lower() != 'blk') and (str(leaveYear).lower() != 'blk'):

        born = ''.join(a for a in str(birthYear) if a.isnumeric())
        born = int(born)

        if type(leaveYear) == datetime.datetime:
            leaveYear.strftime('%Y-%m-%d')

        left = ''.join(l for l in str(leaveYear) if l.isnumeric())
        if left != '':
            left = int(left[0:4])
            calculated_age = left - born
            # print(f'Born: {born}, Left: {left}, Calculated age: {calculated_age}')

            if calculated_age > 0 and calculated_age < 150:
                return calculated_age


def remove_example_mariners():
    # make copy of data into another collection -> backup incase data is lost from original
    db.olk11ShipsData.aggregate(
        [{"$match": {}}, {"$out": "clean_mariners_data"}])

    collection = db['clean_mariners_data']

    collection.update_many(
        {}, {"$pull": {"mariners": {"name": {"$in": ["John Williams", "Edward Jones"]}}}})

    # removes ship records with empty crewlist
    collection.delete_many({"mariners": {"$exists": "true", "$size": 0}})

    return collection


def group_by_rank():

    ships = remove_example_mariners()

    mariners = ships.aggregate([
        {
            "$unwind": "$mariners"
        },
        {
            "$group": {
                "_id": "$mariners.this_ship_capacity",
                "sailors": {
                    "$push": {
                        "age": "$mariners.age",
                        "born": "$mariners.year_of_birth",
                        "leave_date": "$mariners.this_ship_leaving_date",
                        "name": "$mariners.name",
                        "place_of_birth": "$mariners.place_of_birth"
                    }
                }
            }
        }
    ])

    return mariners


def age_at_ranks(mariners):
    ranks = {}
    for doc in mariners:

        if doc['_id'] is not None:

            cleaned = clean_rank(doc['_id'])

            rank_ages = []
            for mariner in doc['sailors']:
                # print(mariner)
                m = Mariner()
                try:
                    if type(mariner['age']) == int:
                        age = mariner['age']
                        m.setAge(age)
                    else:
                        try:
                            calculated_age = calculate_age(
                                birthYear=mariner['born'], leaveYear=mariner['leave_date'])
                        except Exception as e:
                            print(doc['_id'], mariner, e)
                        # m.setAge(calculated_age)
                        if not calculated_age == None:
                            # rank_ages.append(calculated_age)
                            m.setAge(calculated_age)

                    m.setRank(cleaned)
                    m.setName(mariner['name'])
                    m.setPlaceofBirth(mariner['place_of_birth'])

                    if (type(m.age) == int and m.age < 10) and m.rank == "master":
                        print(mariner)
                        print(m.toString())
                    else:
                        rank_ages.append(m)

                    # if m.age == 'missing':
                    #     print(mariner)
                    #     print(m.toString())

                except KeyError:
                    pass

            unique_mariners = []
            for i in rank_ages:
                if i not in unique_mariners:
                    unique_mariners.append(i)

            if cleaned in ranks:
                for sailor in unique_mariners:
                    ranks[cleaned].append(sailor.age)
            else:
                ranks[cleaned] = [i.age for i in unique_mariners]

    return ranks


def boxplot_age_ranks(data):
    labels, ages = data.keys(), data.values()

    newages = [[i for i in rank if type(i) == int] for rank in ages]

    newlabels = []
    for i, label in enumerate(labels):
        new = f"{str(len(newages[i]))} - {label}"
        newlabels.append(new)

    plt.boxplot(newages)
    plt.xticks(range(1, len(newlabels)+1), newlabels)
    plt.xticks(rotation=90)
    plt.ylabel("Age")
    plt.xlabel("Rank")
    plt.show()


def hist_ranks(data):
    rank_freq = {}
    for rank in data:
        rank_freq[rank] = len(data[rank])

    # print(rank_freq)

    plt.bar(range(len(rank_freq)), list(rank_freq.values()))
    plt.xticks(range(len(rank_freq)), list(rank_freq.keys()), rotation=90)
    plt.show()


def distribution_of_ages():
    remove_example_mariners()
    grouped_ranks = group_by_rank()
    rank_ages = age_at_ranks(grouped_ranks)
    boxplot_age_ranks(rank_ages)
    hist_ranks(rank_ages)


def vessel_barchart():
    ships = db.olk11ShipsData.aggregate([
        {
            "$group":
            {"_id": "$vessel name",
             "count": {"$sum": 1}},
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


def ships():
    ships = remove_example_mariners()
    ports = ships.aggregate([
        {"$unwind": "$mariners"
         },
        {"$group": {
            "_id": {
                "ship": "$vessel name",
                "port": "$mariners.this_ship_joining_port",
                "crew": "$mariners"
            }
        }
        },
        {"$group": {
            "_id": {
                "ship": "$_id.ship",
                "port": "$_id.port"
            },
            "crewData": {"$push": {
                "joiningDate": "$_id.crew.this_ship_joining_date",
                "leavingDate": "$_id.crew.this_ship_leaving_date"
            }
            }
        }
        },
        {"$sort": {
            "_id.ship": 1,
            "_id.port": 1
        }
        }
    ])
    
    for thing in ports:
        pprint.pprint(thing)


if __name__ == '__main__':
    #distribution_of_ages()

    ships()

    # cursor = db.clean_mariners_data.find()
    # count = 0
    # for record in cursor:
    #     count += 1

    # print("Number of shipping records: ", count)
