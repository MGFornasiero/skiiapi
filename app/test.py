from typing import Union
import os
import json
import psycopg2
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

from models import Target