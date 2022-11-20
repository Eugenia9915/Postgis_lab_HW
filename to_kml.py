#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Before you can use this script, you need to load an aggregate function e.g.
CREATE AGGREGATE textcat_all(
  basetype    = text,
  sfunc       = textcat,
  stype       = text,
  initcond    = ''
);
http://stackoverflow.com/questions/43870/
how-to-concatenate-strings-of-a-string-field-in-a-postgresql-group-by-query
"""

# To connect to Postgresql
import psycopg2

host = "localhost"
dbname = "test"
username = "postgres"
password = "8845123"

# Connect to an existing database
conn = psycopg2.connect("host=" + host + " dbname=" + dbname
                        + " user=" + username + " password=" + password)

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute("select ST_AsKML(ST_AsText(popu.geom))"
            +" from ne_10m_populated_places as popu"
            +" join ne_10m_railroads as rail"
            +" on ST_DWithin(rail.geom,popu.geom,100)"
            +" group by popu.geom, popu.name"
            +" order by popu.name asc"
            +" limit 10"
            +" ;"
            )
kmlstring = cur.fetchall()

f = open('test.kml', 'w')

for i in range(len(kmlstring)):
    f.write(kmlstring[i][0])
# print (kmlstring[0])
# f.write(kmlstring)

f.close()

# Make the changes to the database persistent
#conn.commit() # Here a as reminder

# Close communication with the database
cur.close()
conn.close()