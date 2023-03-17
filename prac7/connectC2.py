from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

USERNAME = 'XXXXX'
PASSWORD = 'XXXXXXXXX'

#define the authentication details
auth_provider = PlainTextAuthProvider(
        username=USERNAME,
        password=PASSWORD
)

#define the connection details
cluster = Cluster(
        ['nosql.dcs.aber.ac.uk'],
        auth_provider=auth_provider
)

#Create a session variable that holds the connection to the database
session=cluster.connect()

#Set the session to use your keyspace
session.set_keyspace(USERNAME)

#define a function to print out the results of a query.
def show_query():
    rows = session.execute ('SELECT * FROM emp')
    for row in rows:
        print(row.emp_id, row.emp_city, row.emp_name, row.emp_phone)

#call the function
show_query()

#######insert data#######

#define data
emp_id = 56
emp_city = 'Helsinki'
emp_name = 'Sari'
emp_phone = 8569

#define function (that takes the data)
def get_insert(emp_id, emp_city, emp_name, emp_phone):
    insert_query = session.prepare("\
        INSERT INTO emp (emp_id, emp_city, emp_name, emp_phone)\
            VALUES (?,?,?,?)\
        ")

    session.execute(insert_query, [emp_id, emp_city, emp_name, emp_phone])

#call the function with the data   
get_insert(emp_id, emp_city, emp_name, emp_phone)
show_query()

