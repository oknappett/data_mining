from pymongo import MongoClient
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import doctest

# Mongodb user details for olk11
mongoUser = 'olk11'
mongoPass = '7LwEV4mUxIqd'
client = MongoClient(
    f'mongodb://{mongoUser}:{mongoPass}@nosql.dcs.aber.ac.uk/{mongoUser}')
db = client.olk11


### PART 1 ###

class Mariner:
    """
    A class representing a mariner.

    Attributes:
        rank (str): The rank of the mariner.
        age (str): The age of the mariner.
        name (str): The name of the mariner.
        PlaceOfBirth (str): The place of birth of the mariner.

    Methods:
        __init__(self, rank='missing', age='missing', name='missing', PlaceOfBirth='missing'): Initializes a Mariner instance with default values if none are provided.
        __eq__(self, other): Determines if two Mariner instances are equal.
        setAge(self, age): Sets the age of the mariner.
        setRank(self, rank): Sets the rank of the mariner.
        setName(self, name): Sets the name of the mariner.
        setPlaceofBirth(self, PoB): Sets the place of birth of the mariner.
        toString(self): Returns a string representation of the mariner.

    >>> m1 = Mariner()
    >>> m1.toString()
    'Name:missing Age:missing Rank:missing Born:missing'

    >>> m2 = Mariner('captain', '45', 'John', 'London')
    >>> m2.toString()
    'Name:John Age:45 Rank:captain Born:London'

    >>> m3 = Mariner('captain', '45', 'John', 'London')
    >>> m2 == m3
    True

    >>> m4 = Mariner('captain', '45', 'John', 'New York')
    >>> m2 == m4
    False
    """

    def __init__(self, rank='missing', age='missing', name='missing', PlaceOfBirth='missing'):
        """
        Initializes a new instance of the Mariner class with the specified attributes.

        Args:
            rank (str, optional): The rank of the mariner. Defaults to 'missing'.
            age (str, optional): The age of the mariner. Defaults to 'missing'.
            name (str, optional): The name of the mariner. Defaults to 'missing'.
            PlaceOfBirth (str, optional): The place of birth of the mariner. Defaults to 'missing'.
        """
        self.rank = rank
        self.age = age
        self.name = name
        self.PlaceofBirth = PlaceOfBirth

    def __eq__(self, other):
        """
        Determines if two Mariner instances are equal.

        Args:
            other (Mariner): The other instance to compare to.

        Returns:
            bool: True if the instances are equal, False otherwise.
        """
        return self.rank == other.rank and self.age == other.age and self.name == other.name and self.PlaceofBirth == other.PlaceofBirth

    def setAge(self, age):
        """
        Sets the age of the mariner.

        Args:
            age (str): The new age of the mariner.
        """
        self.age = age

    def setRank(self, rank):
        """
        Sets the rank of the mariner.

        Args:
            rank (str): The new rank of the mariner.
        """
        self.rank = rank

    def setName(self, name):
        """
        Sets the name of the mariner.

        Args:
            name (str): The new name of the mariner.
        """
        self.name = name

    def setPlaceofBirth(self, PoB):
        """
        Sets the place of birth of the mariner.

        Args:
            PoB (str): The new place of birth of the mariner.
        """
        self.PlaceofBirth = PoB

    def toString(self):
        """
        Converts mariner object to string format.
        """
        return f"Name:{self.name} Age:{self.age} Rank:{self.rank} Born:{self.PlaceofBirth}"


def clean_rank(rank):
    '''
    Function to clean ranks. Groups ranks together to eliminate messy data such as spelling

    Parameters:
    rank (str): Rank of the individual.

    Returns:
    str: Cleaned rank.

    Examples:
        >>> clean_rank('cookstewardandseaman')
        'steward'
        >>> clean_rank('captain')
        'captain'
        >>> clean_rank('MasterC')
        'master'
        >>> clean_rank('carpenterableseaman')
        'carpenter'
        >>> clean_rank('blk')
        'other'
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


def calculate_time(startYear, endYear):
    '''
    Calculate age from birth year and leave year.

    Args:
        startYear (int or datetime.datetime): Year of birth as integer or datetime object.
        endYear (int or datetime.datetime): Year of leaving as integer or datetime object.

    Returns:
        int: Calculated age based on given birth year and leave year.

    Example:
        >>> calculate_time(1990, 2020)
        30

    '''

    # check if input is not blank
    if (str(startYear).lower() != 'blk') and (str(endYear).lower() != 'blk'):

        # turn datetime objects to string, format Year, month, day
        if type(startYear) == datetime.datetime:
            startYear = startYear.strftime('%Y-%m-%d')

        # remove all characters that aren't numeric
        born = ''.join(a for a in str(startYear) if a.isnumeric())
        born = int(born)

        # turn datetime objects to string, format Year, month, day
        if type(endYear) == datetime.datetime:
            endYear = endYear.strftime('%Y-%m-%d')

        # remove all none numeric characters in leave date
        left = ''.join(l for l in str(endYear) if l.isnumeric())

        # if not blank
        if left != '' and born != '':
            # extract year from date string
            left = int(left[0:4])
            # take age as date leaving the ship - year of birth
            calculated_age = left - born

            # sometimes this doesn't work as the year is recorded wrong
            # remove all ages that aren't possible
            if calculated_age > 0 and calculated_age < 150:
                return calculated_age


def group_by_rank():
    """
    Mongodb aggregation to group mariners by rank

    Returns:
        Mongodb cursor: list of mariners grouped by rank. 
                            Data projected: rank, age, born, leave date, name and place of birth
    """
    mariners = db.olk11ShipsData.aggregate([
        # unwind mariners into an array
        {
            "$unwind": "$mariners"
        },
        # select all mariners that aren't named John Williams and Edward Jones
        # as these are the example mariners and not always removed
        {
            "$match": {
                "mariners.name": {
                    "$nin": [
                        "John Williams",
                        "Edward Jones"
                    ]
                }
            }
        },
        # group mariners by rank and show name, birth year, place of birth and leave date
        # to allow the code to differentiate between different mariners
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
    '''
    Groups mariners by rank and calculates their age at the time they served at that rank.

    Parameters:
        mariners (dict): The list of mariners.

    Returns:
        dict: A dictionary that contains each rank with the corresponding list of ages for mariners that served at that rank.

    Examples:
        >>> mariners = [
        ...     {
        ...         "_id": "Master",
        ...         "sailors": [
        ...             {
        ...                 "age": 28,
        ...                 "born": 1863,
        ...                 "leave_date": "1909-03-08",
        ...                 "name": "John Smith",
        ...                 "place_of_birth": "New York, USA"
        ...             },
        ...             {
        ...                 "age": "missing",
        ...                 "born": 1863,
        ...                 "leave_date": "1909-03-08",
        ...                 "name": "William Johnson",
        ...                 "place_of_birth": "Boston, USA"
        ...             }
        ...         ]
        ...     },
        ...     {
        ...         "_id": "Seaman",
        ...         "sailors": [
        ...             {
        ...                 "age": 22,
        ...                 "born": 1877,
        ...                 "leave_date": "1899-08-16",
        ...                 "name": "James Davis",
        ...                 "place_of_birth": "Liverpool, England"
        ...             }
        ...         ]
        ...     }
        ... ]
        >>> age_at_ranks(mariners)
        {'master': [28, 46], 'ordinary seaman': [22]}
    '''
    ranks = {}

    # loop through all ranks in mariner list
    for doc in mariners:

        # check if rank is not none
        if doc['_id'] is not None:

            # clean rank string
            cleaned = clean_rank(doc['_id'])

            # Create an empty list to store the ages of the mariners who served at that rank.
            rank_ages = []

            # loop through all sailors at rank
            for mariner in doc['sailors']:
                # create new instance of mariner object
                m = Mariner()
                try:
                    # if age of sailor is int, set the age
                    if type(mariner['age']) == int:
                        age = mariner['age']
                        m.setAge(age)
                    else:
                        try:
                            # if age is not an integer, calculate it from birth date and leaving ship date
                            calculated_age = calculate_time(
                                startYear=mariner['born'], endYear=mariner['leave_date'])
                            # if age is sucsessfully calculated, set this to the age
                            if not calculated_age == None:
                                m.setAge(calculated_age)
                        except Exception as e:
                            # If there is an error while calculating the age, print the rank, sailor and the error message.
                            print(doc['_id'], mariner, e)
                        # m.setAge(calculated_age)

                    m.setRank(cleaned)
                    m.setName(mariner['name'])
                    m.setPlaceofBirth(mariner['place_of_birth'])

                    # if age of rank less than 10, print mariner
                    # done as in a plot, one sailor with master rank is apparently 7 years old
                    if (type(m.age) == int and m.age < 10):
                        print(mariner)
                        print(m.toString())
                    else:
                        rank_ages.append(m)

                except KeyError:
                    pass

            # remove duplicate mariners
            # duplicate mariners decided by __eq__ in mariner class
            # duplicate if age, name and place of birth the same
            unique_mariners = []
            for i in rank_ages:
                if i not in unique_mariners:
                    unique_mariners.append(i)

            # add age to total count
            if cleaned in ranks:
                for sailor in unique_mariners:
                    ranks[cleaned].append(sailor.age)
            else:
                ranks[cleaned] = [i.age for i in unique_mariners]

    return ranks


def boxplot_age_ranks(data):
    """
    Creates a boxplot of the age distribution for each rank in the given data.

    Parameters:
        data (dict): A dictionary containing rank names as keys and lists of ages as values.

    Returns:
        None.

    Example:
        data = {'Master': [28, 32, 41, 36, 27], 'Seaman': [22, 23, 26, 24], 'Mate': ['missing', 38, 30, 44, 32, 28, 39, 34]}
        boxplot_age_ranks(data) Displays a boxplot of age distribution for each rank in data
    """
    labels, ages = data.keys(), data.values()

    # create list of ages that only includes integer values
    newages = [[i for i in rank if type(i) == int] for rank in ages]

    # new list of labels that includes the count of ages at each rank
    newlabels = []
    for i, label in enumerate(labels):
        new = f"{str(len(newages[i]))} - {label}"
        newlabels.append(new)

    # box plot each rank to see distribution of ages at each rank
    plt.boxplot(newages)
    plt.xticks(range(1, len(newlabels)+1), newlabels)
    plt.xticks(rotation=90)
    plt.ylabel("Age")
    plt.xlabel("Rank")
    plt.title("Distribution of ages at each rank")
    plt.show()


def hist_ranks(data):
    """
    Plots a histogram of the frequency of mariners in each rank.

    Parameters:
        data (dict): A dictionary with ranks as keys and corresponding list of ages for mariners.

    Returns:
        None

    Examples:
        data = {'Master': [28], 'Seaman': [22]}
        hist_ranks(data) Plots histogram of frequency of mariners in each rank
    """
    # empty dictionary to store frequency at each rank
    rank_freq = {}

    # add frequencies for each rank
    for rank in data:
        rank_freq[rank] = len(data[rank])

    # bar chart the frequencies
    plt.bar(range(len(rank_freq)), list(rank_freq.values()))
    plt.xticks(range(len(rank_freq)), list(rank_freq.keys()), rotation=90)
    plt.xlabel("Ranks")
    plt.title("Frequency")
    plt.show()


def distribution_of_ages():

    # group mariners by rank
    grouped_ranks = group_by_rank()

    # get age of mariners at each rank
    rank_ages = age_at_ranks(grouped_ranks)

    # plot boxplot of ages for each rank
    boxplot_age_ranks(rank_ages)

    # plot historgram of frequency of ages at each rank
    hist_ranks(rank_ages)

#### PART 2 ####


def ships_and_ports():
    """
    Aggregate data to retrieve the ports each ship visited 
    and the crew  data for each port. The crew data includes
    the joining date and leaving date for each mariner.

    Returns:
        mongodb cursor: The result of the aggregation pipeline.
    """
    ports = db.olk11ShipsData.aggregate([
        # Split the mariners array into individual documents
        {"$unwind": "$mariners"
         },
        # Exclude mariners with names John Williams and Edward Jones
        {
            "$match": {
                "mariners.name": {
                    "$nin": [
                        "John Williams",
                        "Edward Jones"
                    ]
                }
            }
        },
        # exclude mariners who's joining port is blank
        {"$match": {
            "mariners.this_ship_joining_port": {
                "$ne": "blk"
            }
        }
            # group ship names, and join date and mariners
        },
        {"$group": {
            "_id": {
                "ship": "$vessel name",
                "port": "$mariners.this_ship_joining_port",
                "crew": "$mariners"
            }
        }
        },
        # group again by ship name and last port visited
        {"$group": {
            "_id": {
                "ship": "$_id.ship",
                "port": "$_id.port"
            },
            # create new list of mariners
            "crewData": {"$push": {
                "joiningDate": "$_id.crew.this_ship_joining_date",
                "leavingDate": "$_id.crew.this_ship_leaving_date"
            }
            }
        }
        },
        # sort by name of ship for testing
        {"$sort": {
            "_id.ship": 1,
        }
        }
    ])

    return ports


def clean_port(port):
    """
    Function to clean ranks. Groups ranks together to eliminate messy data such as spelling

    Parameters:
    port (str): A string representing the name of a port.

    Returns:
    str: The standardized name of the port.

    Example:
        >>> clean_port('NewportMonmouthshire')
        'newport'
        >>> clean_port('Caernarvon')
        'caernarvon'
    """

    # strip all characters that aren't letters
    port = ''.join(a for a in str(port) if a.isalpha()).lower()

    # switch case for string
    match port:
        case aberaeron if aberaeron in ['aberaeron', 'aberayron']:
            cleaned = 'aberaeron'

        case aberdovey if aberdovey in ['aberdovey', 'aberdyfi']:
            cleaned = 'aberdovey'

        case aberystywth if aberystywth in ['aberystwith', 'aberystwyth', 'aberystywith', 'aberyswtih']:
            cleaned = 'aberystywth'

        case barry if barry in ['barry', 'barryport']:
            cleaned = 'barry'

        case britton if britton in ['britonferry', 'brittonferry']:
            cleaned = 'brittonferry'

        case caernarfon if caernarfon in ['caernarfon', 'caernarvon']:
            cleaned = 'caernarvon'

        case gloucester if gloucester in ['gloster', 'gloucester']:
            cleaned = 'gloucester'

        case kingston if kingston in ['kingston', 'kingstown']:
            cleaned = 'kingstown'

        case llanelli if llanelli in ['llanelli', 'llanelly']:
            cleaned = 'llanelli'

        case middlesborough if middlesborough in ['middlesborough', 'middlesbro', 'middlesbrough']:
            cleaned = 'middlesborough'

        case newport if newport in ['newport', 'newportmon', 'newportmonmouthshire', 'newportpralt']:
            cleaned = 'newport'

        case newquay if newquay in ['newqua', 'newquay', 'newquayaberystwyth', 'newquaycardigan']:
            cleaned = 'newquay'

        case porthmadog if porthmadog in ['porthmadoc', 'porthmadog', 'portmadoc', 'portmadog']:
            cleaned = 'porthmadog'

        case _:
            cleaned = port

    return cleaned


def plot_ports(ports):
    """
    Plots the number of visits to different ports.

    Args:
    - ports: A list of dictionaries, each dictionary contains information about a ship's visit to ports.

    Example:
        ports = [
            {"_id": {"ship": "ship1", "port": "aberystwith"}},
            {"_id": {"ship": "ship2", "port": "barry"}},
            {"_id": {"ship": "ship3", "port": "newport"}},
            {"_id": {"ship": "ship4", "port": "newport"}},
            {"_id": {"ship": "ship5", "port": "newport"}}
        ]
        plot_ports(ports) plots a boxplot and bar chart of port visits
    """
    # create a dictionary to count the number of visits to each port
    port_count = {}
    for data in ports:
        ship = data["_id"]
        if "port" in ship:
            extracted_port = ship["port"]
            port = clean_port(extracted_port)
            if port in port_count:
                port_count[port] += 1
            else:
                port_count[port] = 1

    # list of visit counts
    counts = port_count.values()

    # boxplot number of visits to each port
    # line at 25 to show where the amount of visits stops being so grouped together
    # this is the metric decided to plot ports
    # it was originally decided to be all outlying ports but it still groups a bit
    plt.axhline(y=25, color='r', linestyle=':')
    plt.boxplot(counts, labels=[""])
    plt.ylabel("Number of visits")

    plt.title("Box plot of amount of port visits\nto decide which ones to plot")
    plt.show()

    # create dict of ports with more than 25 visits
    plot_port = {}
    for p in port_count:
        if port_count[p] > 25:
            plot_port[p] = port_count[p]

    plot_port.pop("continued")

    # plot the ports
    plt.bar(range(len(plot_port)), list(plot_port.values()))
    plt.xticks(range(len(plot_port)), list(plot_port.keys()), rotation=90)
    plt.xlabel("Ports")
    plt.ylabel("Number of visits")
    plt.title("Number of visits for ports")
    plt.show()


def remove_outliers(data):
    """
    This function takes in a list of numerical data and removes any outliers.

    Args:
        data (list): A list of numerical data

    Returns:
        list: A list of data with any outliers removed

    Example:
        >>> remove_outliers([1, 2, 3, 200, 300, 4, 5, 6])
        [1, 2, 3, 4, 5, 6]
    """
    # Calculate the mean and standard deviation of the data
    mean = np.mean(data)
    q1, q3 = np.percentile(data, [25, 75])
    iqr = q3-q1

    # Calculate the upper and lower bounds for identifying outliers
    upperbound = mean + 1.5*iqr
    lowerbound = mean - 1.5*iqr

    # Create a list to store the data without outliers
    out = []

    # Iterate through the data, checking if each value is an outlier
    for obj in data:
        if obj > lowerbound and obj < upperbound:
            out.append(obj)

    # Return the list of data without outliers
    return out


def length_of_service(crews):
    """
    Calculates the average length of service for each crew member in a list of crews. 
    It removes any outliers and plots the density of average crew length.

    Args:
        crews (list): A list of dictionaries representing crews.

    Example:
        crews = [{'crewData': [{'joiningDate': '2022-01-01', 'leavingDate': '2022-01-15'},
                                {'joiningDate': '2022-01-15', 'leavingDate': '2022-01-30'}]},
                 {'crewData': [{'joiningDate': '2022-02-01', 'leavingDate': '2022-02-15'},
                                {'joiningDate': '2022-02-15', 'leavingDate': '2022-03-01'},
                                {'joiningDate': '2022-03-01', 'leavingDate': '2022-03-15'}]}]
        length_of_service(crews) creates density plot
    """

    service_times = []

    # Iterate through each crew and calculate the length of service for each individual crew member
    for doc in crews:
        crew_lengths = []

        for mariner in doc['crewData']:
            if all(k in mariner for k in ("joiningDate", "leavingDate")):
                join = str(mariner['joiningDate'])
                leave = str(mariner['leavingDate'])

                testjoin = ''.join(a for a in str(join) if a.isnumeric())
                testleave = ''.join(a for a in str(leave) if a.isnumeric())

                # Check if the cleaned up dates are not empty strings. Checks if dates contain numbers
                if testjoin != '' and testleave != '':
                    try:
                        # Convert date strings to datetime objects
                        join = datetime.datetime.strptime(
                            join, "%Y-%m-%d").date()
                        leave = datetime.datetime.strptime(
                            leave, "%Y-%m-%d").date()

                        # calculate length of service in days
                        length = (leave-join).days

                        # If the length of service is negative, it means the leaving date is before the joining date
                        # In that case, we take the absolute value of the length of service
                        if length < 0:
                            length = abs(length)

                        # show crews over length of 1000
                        if length > 1000:
                            print(f"{leave} - {join} = {length} days")

                        crew_lengths.append(length)

                    except:
                        pass

        # Calculate the average length of service for the crew if the crew has at least one member with valid length of service
        if len(crew_lengths) > 0:
            crew_avg = np.mean(crew_lengths)
            service_times.append(crew_avg/31)

    # remove outliers for plot
    no_outs = remove_outliers(service_times)
    # plot density and curve
    sns.histplot(data=no_outs, bins=int(max(no_outs)),
                 stat="density", alpha=0.04, kde=True)
    plt.xlabel("Months of service")
    plt.title("Densisty of average crew length")
    plt.show()
    print(min(no_outs), max(no_outs))

def distribution_of_crews():
    crews = ships_and_ports()
    length_of_service(crews)
    crews = ships_and_ports()
    plot_ports(crews)

def main():
    distribution_of_ages()
    distribution_of_crews()

def remove_example_mariners():
    '''
    Remove John Williams and Edward Jones for testing purposes. 
    '''
    # make copy of data into another collection -> backup incase data is lost from original
    db.olk11ShipsData.aggregate(
        [{"$match": {}}, {"$out": "clean_mariners_data"}])

    collection = db['clean_mariners_data']

    collection.update_many(
        {}, {"$pull": {"mariners": {"name": {"$in": ["John Williams", "Edward Jones"]}}}})

    # removes ship records with empty crewlist
    collection.delete_many({"mariners": {"$exists": "true", "$size": 0}})

    return collection

def initialPlots():
    '''
    Initial plots of the data before cleaning/handling noise in data
    Used for visualisation and explanation of how the data is handled later
    '''
    # ===part 1:individual stories===
    # ages = db.olk11ShipsData.aggregate([
    #     {
    #         "$unwind": "$mariners"
    #     },
    #     {
    #         "$group": {
    #             "_id": "$mariners.age",
    #             "count": {
    #                 "$sum": 1
    #             }
    #         }
    #     }
    # ])

    # ages_freq = {}

    # for doc in ages:
    #     if type(doc["_id"]) == int:
    #         ages_freq[doc['_id']] = int(doc['count'])

    # print(ages_freq)
    # plt.bar(ages_freq.keys(), ages_freq.values())
    # plt.title("Original Raw data plot of age distribution for all mariners")
    # plt.ylabel("No. Mariners")
    # plt.xlabel("Age")
    # plt.savefig("assignment/plots/data_exploration/Raw_age_dist.png")
    # plt.show()

    # ages_no_johnedward = db.olk11ShipsData.aggregate([
    #     {
    #         "$unwind": "$mariners"
    #     },
    #     {
    #         "$match": {
    #             "mariners.name": {
    #                 "$nin": [
    #                     "Edward Jones",
    #                     "John Williams"
    #                 ]
    #             }
    #         }
    #     },
    #     {
    #         "$group": {
    #             "_id": "$mariners.age",
    #             "count": {
    #                 "$sum": 1
    #             }
    #         }
    #     }
    # ])

    # clean_ages_freq = {}

    # for doc in ages_no_johnedward:
    #     if type(doc["_id"]) == int:
    #         clean_ages_freq[doc['_id']] = int(doc['count'])

    # print(clean_ages_freq)
    # plt.bar(clean_ages_freq.keys(), clean_ages_freq.values())
    # plt.title(
    #     "Data plot of age distribution for all mariners\nnot named John Williams or Edward Jones")
    # plt.ylabel("No. Mariners")
    # plt.xlabel("Age")
    # plt.savefig("assignment/plots/data_exploration/clean_age_dist.png")
    # plt.show()

    # raw_ranks = db.olk11ShipsData.aggregate([
    #     {
    #         "$unwind": "$mariners"
    #     },
    #     {
    #         "$match": {
    #             "mariners.name": {
    #                 "$nin": [
    #                     "Edward Jones",
    #                     "John Williams"
    #                 ]
    #             }
    #         }
    #     },
    #     {
    #         "$group": {
    #             "_id": "$mariners.this_ship_capacity",
    #             "count": {
    #                 "$sum": 1
    #             }
    #         }
    #     }
    # ])

    # raw_ranks_freq = {}
    # clean_ranks_freq = {}
    # for doc in raw_ranks:
    #         raw_ranks_freq[doc['_id']] = int(doc['count'])
    #         cleaned = clean_rank(doc["_id"])
    #         if cleaned in clean_ranks_freq:
    #             clean_ranks_freq[cleaned] += doc['count']
    #         else:
    #             clean_ranks_freq[cleaned] = doc['count']

    # print(raw_ranks_freq)

    # print(clean_ranks_freq)

    # raw_ranks = len(list(raw_ranks_freq.values()))
    # clean_ranks = len(list(clean_ranks_freq.values()))

    # plt.bar([f"{raw_ranks} raw", f"{clean_ranks} cleaned"],[raw_ranks,clean_ranks])
    # plt.title("Number of unique ranks before and after cleaning")
    # plt.ylabel("Amount of ranks")
    # plt.savefig("assignment/plots/data_exploration/clean_vs_raw_ranks.png")
    # plt.show()

    raw_ports = db.olk11ShipsData.aggregate([
        {
            "$unwind": "$mariners"
        },
        {
            "$match": {
                "mariners.name": {
                    "$nin": [
                        "Edward Jones",
                        "John Williams"
                    ]
                }
            }
        },
        {
            "$group": {
                "_id": "$mariners.this_ship_leaving_port",
                "count": {
                    "$sum": 1
                }
            }
        }
    ])

    raw_ports_freq = {}
    clean_ports_freq = {}
    for doc in raw_ports:
        raw_ports_freq[doc['_id']] = int(doc['count'])
        cleaned = clean_port(doc["_id"])
        if cleaned in clean_ports_freq:
            clean_ports_freq[cleaned] += doc['count']
        else:
            clean_ports_freq[cleaned] = doc['count']

    print(raw_ports_freq)

    print(clean_ports_freq)

    raw_ports = len(list(raw_ports_freq.values()))
    clean_ports = len(list(clean_ports_freq.values()))

    plt.bar([f"{raw_ports} raw", f"{clean_ports} cleaned"],
            [raw_ports, clean_ports])
    plt.title("Number of unique ports before and after cleaning")
    plt.ylabel("Amount of ports")
    plt.savefig("assignment/plots/data_exploration/clean_vs_raw_ports.png")
    plt.show()

    # ===part 2:who is visiting===
    # plot ship data
    # plot length of service of crew -> date between joining and leaving
    # plot number of ship visits to each port that inst aberystwyth


if __name__ == '__main__':
    # main()
    #distribution_of_ages()
    #initialPlots()
    # uncomment to run doctest
    doctest.testmod(verbose=True)
