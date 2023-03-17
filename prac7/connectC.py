from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

USERNAME = 'olk11'
PASSWORD = '7LwEV4mUxIqd'

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
