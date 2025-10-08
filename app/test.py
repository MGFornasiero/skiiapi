from typing import Union
import os
import json
import psycopg2


from .models import Target # ski.targets() , public.get_targets(), public.get_target_info(), public.qry_ts_targets()
from .models import StrikingPart # ski.strikingparts() , public.get_strikingparts(), public.get_strikingparts_info(), public.qry_ts_strikingparts()
from .models import Stand # ski.stands() , public.get_stands(), public.get_stand_info(), public.qry_ts_stands()
from .models import Grade # ski.grades() , public.get_grade()
from .models import KihonInventory # ski.kihon_inventory() , public.get_kihons()
from .models import KihonTx #get_kihon_tx()
from .models import KihonStep  #get_kihon_steps()
from .models import KihonFormatted  #kihon_frmlist()
from .models import KataInventory  # ski.kata_inventory() , public.show_katainventory(), public.get_katainfo()
from .models import KataSequenceStep  #get_katasequence()
from .models import BunkaiInventory  # ski.bunkai_inventory() , public.get_katabunkais()

uri = os.environ['SKIURI']





kata_id = 2
print("\n")
print("\n")
conn = psycopg2.connect(uri)
cur = conn.cursor()
cur.execute(f"SELECT id_bunkai, kata_id, version, name, description, notes,resources, resource_url FROM public.get_katabunkais({kata_id});")
result = cur.fetchall()
bunkai_info = {
    res[0]:{"kata_id":res[1],"version":res[2],"name":res[3],"description":res[4],"notes":res[5],"resources":res[6],"resource_url":res[7]} for res in result
} # da implementare nel json di ritorno
print(bunkai_info)

print("\n")
cur.execute(f"SELECT id_bunkai,version,name,description,notes,resources FROM public.get_katabunkais({kata_id});")
bunkais_result = cur.fetchall()
bunkai_ids  = {
    res[0]:{"version":res[1],"name":res[2],"description":res[3],"notes":res[4],"resources":res[5]} for res in bunkais_result
} # da implementare nel json di ritorno
print(bunkai_ids)
bunkai_id = 2

import psycopg2.pool

# Create a connection pool with a minimum of 2 connections and
#a maximum of 3 connections
pool = psycopg2.pool.SimpleConnectionPool(
    1, 5, uri
)

# Get a connection from the pool
with my_pool.connection() as conn:
    conn.execute(...)

# Use the connection to execute a query
cursor = connection1.cursor()
print("Results from Connection1: \n")
cursor.execute('SELECT * FROM person ORDER BY id')
results = cursor.fetchall()
for data in results:
    print(data)
    print()

connection2 = pool.getconn()

# Use the connection to execute a query
cursor = connection2.cursor()
print("Results from Connection2: \n")
cursor.execute('SELECT * FROM person ORDER BY id')
results = cursor.fetchall()
for data in results:
    print(data)
    print()

connection3 = pool.getconn()

# Use the connection to execute a query
cursor = connection3.cursor()
print("Results from Connection3: \n")
cursor.execute('SELECT * FROM person ORDER BY id')
results = cursor.fetchall()
for data in results:
    print(data)
    print()

# Since maximum number of connections in the pool #
#is 3 and three connections 
#are already made and not released yet. 
#So, requesting for a fourth connection gives error.

# connection4 = pool.getconn()
# cursor = connection4.cursor()
# print("Results from Connection3: \n")
# cursor.execute('SELECT * FROM person ORDER BY id')
# results = cursor.fetchall()
# for data in results:
#     print(data)
#     print()


# Release the connection back to the pool
pool.putconn(connection1)
pool.putconn(connection2)
pool.putconn(connection3)









