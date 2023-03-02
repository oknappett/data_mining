import pprint

from pymongo import MongoClient
client = MongoClient('mongodb://olk11:7LwEV4mUxIqd@nosql.dcs.aber.ac.uk/olk11')

db = client.olk11

outputfile = open("map_reduce_outputfile", encoding="utf-8", mode="w")

from bson.code import Code

mapper = Code(""" 
    function() {
        this.mariners.forEach( function( mariner ) {
            emit(mariner.name, 1);
        })
    }
""")

reducer = Code("""
    function (key, values) {
        var total = 0;
        for (var i = 0; i < values.length; i++) {
            total += values[i];
        }
    return total;
    }
""")

result = db.olk11.map_reduce(mapper, reducer, "mariner_counts")

for doc in result.find():
    pprint.pprint(doc, outputfile)