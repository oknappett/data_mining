from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

USERNAME = 'XXXXXX'
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

#######Update data#######

#define data
emp_city_NEW = 'Espoo'
emp_id = 5

#define function (that takes the data)
def get_update(**kwargs):
    emp_id = kwargs.pop('emp_id')
    keys, vals = zip(*kwargs.items())
    session.execute(
        'UPDATE emp SET '+' '.join([k + ' = %s' for k in keys]) + 'WHERE emp_id = %s',
        [*vals, emp_id]
        )
     
#call the function with the data        
get_update(emp_city=emp_city_NEW, emp_id = emp_id)
show_query()

