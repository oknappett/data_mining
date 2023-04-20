from pymongo import MongoClient
import pprint
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Mongodb user details for olk11
mongoUser = 'olk11'
mongoPass = '7LwEV4mUxIqd'
client = MongoClient(
    f'mongodb://{mongoUser}:{mongoPass}@nosql.dcs.aber.ac.uk/{mongoUser}')
db = client.olk11


def count_record():
    # the shipping record data is imported into a collection called olk11ShipsData
    # cursor = db.olk11ShipsData.find()
    cursor = db.shipsTest.find()
    count = 0
    for record in cursor:
        count += 1

    print("Number of shipping records: ", count)


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


def clean_mariners():
    # make copy of data into another collection -> backup incase data is lost from original
    db.olk11ShipsData.aggregate(
        [{"$match": {}}, {"$out": "clean_mariners_data"}])

    mycol = db['clean_mariners_data']

    mycol.update_many(
        {}, {"$pull": {"mariners": {"name": {"$in": ["John Williams", "Edward Jones"]}}}})
    # removes ship records with empty crewlist
    mycol.delete_many({"mariners": {"$exists": "true", "$size": 0}})

    mariners = mycol.aggregate([
        {
            "$project": {
                "ship": "$vessel_name",
                "mariners": 1
            }
        },
        {
            "$unwind": "$mariners"  # unwind mariners into array
        },
        {
            "$project": {  # select relavent information
                "name": "$mariners.name",
                "age": "$mariners.age",
                "PoB": "$mariners.place_of_birth",
                "DoB": "$mariners.year_of_birth",
                "leave_date": "$mariners.this_ship_leaving_date"
            }
        },
        {
            "$group": {  # group mariners by values in attempt to remove duplicate inputs
                "_id": {
                    "birthPlace": "$PoB",
                    "name": "$name",
                    "DoB": "$DoB",
                    "age": "$age"
                }
            }
        },
        {
            "$project": {  # output mariner information
                "_id": "$_id.name",
                "age": "$_id.age",
                "DoB": "$_id.DoB",
                "birthPlace": "$_id.birthPlace",
                "leave_date": "$leave_date"
            }
        }
    ])

    marinersdict = {"name": [], "age": [], "birth_year": [],
                    "birth_place": [], "leave_date": []}

    for doc in mariners:
        try:
            this_birthPlace = doc['birthPlace']
            this_name = doc['_id']
            this_age = doc['age']
            this_birthYear = doc['DoB']
            this_leaveDate = doc['leave_date']
        except Exception as e:
            if e == '_id':
                this_name = None
            elif e == 'age':
                this_age = None
            elif e == 'DoB':
                this_birthYear = None
            elif e == 'birthPlace':
                this_birthPlace = None
            elif e == 'leave_date':
                this_leaveDate = None
        finally:
            marinersdict["name"].append(this_name)
            marinersdict["age"].append(this_age)
            marinersdict["birth_year"].append(this_birthYear)
            marinersdict["birth_place"].append(this_birthPlace)
            marinersdict['leave_date'].append(this_leaveDate)

    df = pd.DataFrame.from_dict(marinersdict)
    # cleandf = df.groupby(['name', 'age'])
    dropdf = df.drop_duplicates()
    print(f"Before drop: {len(df)}, after drop: {len(dropdf)}")

    print(list(dropdf['age']))

    return dropdf

def clean_rank(rank):
    '''
    Function to clean ranks. Groups ranks together to eliminate messy data such as spelling
    '''
    #output of ranks, needs to be analysed and changed:
    #dict_keys(['', 'boatswainmaster', 'runner', 'boy', 'stmate', 'master', 'stengineer', 'seaman', 'masterc', 'onlymate', 
    # 'cape', 'mate', 'cooksteward', 'ndmate', 'cookandableseaman', 'mastervolunteerscertificatec', 'boatswain', 'ordinaryseaman', 
    # 'mateableseaman', 'thengineer', 'botswain', 'purser', 'apprentice', 'bosun', 'skipper', 'secondengineer', 'shipkeeper', 
    # 'stoker', 'ableseaman', 'messroomsteward', 'engineersteward', 'bswain', 'ndhand', 'ordinaryseamancook', 'donkeyman', 'cook', 
    # 'cookordinaryseaman', 'cookstewardandseaman', 'rdmate', 'pantryboy', 'fireman', 'mater', 'rdhand', 'steward', 'cookstewardseaman', 
    # 'captainmaster', 'captain', 'ndengineer', 'bargeman', 'rdengineer', 'crengineer', 'cookableseaman', 'carpenterseaman', 'blk', 'cookseaman', 
    # 'cookandsteward', 'bosunandlamps', 'radioofficer', 'lamptrimmer', 'masterowner', 'boson', 'assistantengineer', 'stewardcook', 'helmsman', 'carpenterableseaman', 
    # 'mstr', 'donkeyengineoperator', 'matecc', 'mateboatswain', 'cookboy', 'pantrymanfireman', 'stwck', 'firstmate', 'engineer', 'nil', 'ableseamancook', 'ab', 'matepurser', 
    # 'sl', 'seman', 'ordinary', 'carpenter', 'secondmate', 'boyordinary', 'enigneer', 'mastershipkeeper', 'messroom', 'cabinboy', 'leadingseaman', 'mastercaptain'])
    
    #change rank to single string with only alpha characters
    rank = ''.join(c for c in str(rank) if c.isalpha()).lower()

    #change rank to grouped rank
    match rank:
        case captain if captain in ['skipper', 'captainmaster', 'captain','mastercaptain' ]:
            cleaned = 'captain'
        case purser if purser in ['purser', 'matepurser']:
            cleaned = 'purser'
        case master if master in ['master', 'masterc', 'mater', 'captainmaster', 'mstr', 'mastershipkeeper', 
                                  'mastercaptain', 'mastervolunteerscertificatec']: 
            cleaned = 'master'
        case boatswain if boatswain in ['boatswainmaster','boatswain','botswain', 'bswain', 'mateboatswain']:
            cleaned = 'boatswain'
        case steward if steward in ['cooksteward','messroomsteward', 'engineersteward', 'cookstewardandseaman','steward',
                                     'cookstewardseaman', 'cookandsteward', 'stewardcook', 'stwck']:
            cleaned = 'steward'
        case cook if cook in ['cooksteward', 'ordinaryseamancook', 'cook', 'cookordinaryseaman', 
                                'cookstewardandseaman', 'cookstewardseaman', 'cookableseaman', 
                                'cookseaman', 'cookandsteward','stewardcook',  'cookboy', 'ableseamancook']:
            cleaned = 'cook'
        case carpenter if carpenter in ['carpenterseaman', 'carpenterableseaman', 'carpenter']:
            cleaned = 'carpenter'
        case mate if mate in ['onlymate', 'mate', 'ndmate', 'mateableseaman', 'rdmate', 'matecc', 'firstmate', 
                              'matepurser', 'secondmate', 'stmate']:
            cleaned = 'mate'
        case able if able in ['cookandableseaman','mateableseaman', 'ableseaman', 'cookableseaman','carpenterableseaman',
                              'ableseamancook']:
            cleaned = 'able seaman'
        #seaman = ordinary seaman according to me
        case ordinary if ordinary in ['seaman', 'ordinaryseaman', 'ordinaryseamancook', 'cookordinaryseaman', 'cookstewardandseaman',
                                      'cookstewardseaman', 'cookseaman', 'seman', 'ordinary']:
            cleaned = 'ordinary seaman'
        case boy if boy in ['boy', 'pantryboy', 'cookboy','boyordinary', 'cabinboy' ]:
            cleaned = 'boy'
        case engineer if engineer in ['stengineer', 'thengineer', 'secondengineer', 'engineersteward', 'ndengineer',
                                      'rdengineer', 'crengineer', 'assistantengineer', 'engineer', 'enigneer']:
            cleaned = 'engineer'
        case fireman if fireman in ['fireman','pantrymanfireman']:
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
            #print(f'Born: {born}, Left: {left}, Calculated age: {calculated_age}')
        
        
            if calculated_age>0 and calculated_age<150:
                return calculated_age

def age_at_ranks():
    # make copy of data into another collection -> backup incase data is lost from original
    db.olk11ShipsData.aggregate(
        [{"$match": {}}, {"$out": "clean_mariners_data"}])

    mycol = db['clean_mariners_data']

    mycol.update_many(
        {}, {"$pull": {"mariners": {"name": {"$in": ["John Williams", "Edward Jones"]}}}})
    # removes ship records with empty crewlist
    mycol.delete_many({"mariners": {"$exists": "true", "$size": 0}})

    mariners = mycol.aggregate([
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
                        "name": "$mariners.name"
                    }
                }
            }
        }
    ])

    ranks = {}

    for doc in mariners:
        if doc['_id'] is not None:

            cleaned = clean_rank(doc['_id'])

            rank_ages = []
            for mariner in doc['sailors']:
                try:
                    if type(mariner['age']) == int:
                        rank_ages.append(mariner['age'])
                    else:
                        calculated_age = calculate_age(birthYear = mariner['born'], leaveYear = mariner['leave_date'])
                        
                        if not calculated_age is None:
                            rank_ages.append(calculated_age)
                
                
                except KeyError as ex:
                    #print(f"{mariner}error: {ex}")
                    pass
            #print(rank, ":",rank_ages)
            if cleaned in ranks:
                for age in rank_ages:
                    ranks[cleaned].append(age)
            else:
                ranks[cleaned] = rank_ages
    # for rank in ranks.keys():
    #     print(f"{rank}: {len(ranks[rank])} mariners")
    # print(f"{len(ranks.keys())} unique ranks")
    #print(ranks)

    labels, data = ranks.keys(), ranks.values()

    print(min(ranks['master']), max(ranks['master']))

    # plt.boxplot(data)
    # plt.xticks(range(1, len(labels)+1), labels)
    # plt.xticks(rotation=90)
    # plt.show()
    

    return ranks

def rank_age_box(ranks):
    plt.boxplot([n for v in ranks.values() for n in v])
    plt.show()

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


def mariners_size():
    # db.shipsTest.aggregate([ {$project: {"vessel name": 1, "mariners": , "crew": {$size: "$mariners"}}}, {$match: {"crew": {$gt: 10}}} ]).pretty()

    pass


def age_hist():
    client = MongoClient(
        'mongodb://olk11:7LwEV4mUxIqd@nosql.dcs.aber.ac.uk/olk11')

    db = client.olk11

    # cursor = db.olk11ShipsData.aggregate([{"$match": {"vessel name": "Loyalty"}}])

    # db.shipsTest.updateMany( {}, {$pull: {"mariners": {"name": { $in: ["John Williams", "Edward Jones"]}} } } )
    cursor = db.shipsTest.find()

    # cursor = db.olk11ShipsData.find()

    ages = []

    new_ages = []

    for doc in cursor:
        mariners = doc['mariners']
        for m in mariners:
            # print(m)
            try:
                # if m['name'] not in ['John Williams', 'Edward Jones']:
                if type(m['age']) == int:
                    ages.append(m['age'])
                if m['age'] == 'blk' and 'year_of_birth' in m:
                    if m['this_ship_leaving_date'] != 'blk' and m['year_of_birth'] != 'blk':
                        # new_age = m['this_ship_leaving_date'] - int(m['year_of_birth'])
                        print(m['this_ship_leaving_date'], m['year_of_birth'])
            except KeyError:
                pass
    age_dict = {}

    for age in ages:
        if age in age_dict:
            age_dict[age] += 1
        else:
            age_dict[age] = 1

    # age_dict.pop(35)

    print(len(age_dict), age_dict)

    plt.hist(ages, bins='auto')
    plt.show()


if __name__ == '__main__':
    # age_hist()
    # count_record()
    #clean_mariners()
    age_at_ranks()