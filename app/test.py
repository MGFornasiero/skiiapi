from typing import Union
import os
import json
import sys
import psycopg2

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.models import Target # ski.targets() , public.get_targets(), public.get_target_info(), public.qry_ts_targets()
from app.models import StrikingPart # ski.strikingparts() , public.get_strikingparts(), public.get_strikingparts_info(), public.qry_ts_strikingparts()
from app.models import Stand # ski.stands() , public.get_stands(), public.get_stand_info(), public.qry_ts_stands()
from app.models import Grade # ski.grades() , public.get_grade()
from app.models import KihonInventory # ski.kihon_inventory() , public.get_kihons()
from app.models import KihonTx #get_kihon_tx()
from app.models import KihonStep  #get_kihon_steps()
from app.models import KihonFormatted  #kihon_frmlist()
from app.models import KataInventory  # ski.kata_inventory() , public.show_katainventory(), public.get_katainfo()
from app.models import KataSequenceStep  #get_katasequence()
from app.models import BunkaiInventory  # ski.bunkai_inventory() , public.get_katabunkais()

uri = os.environ['SKIURI']




kata_id = 2
print("\n")
print("\n")


conn = psycopg2.connect(uri)
cur = conn.cursor()
cur.execute("SELECT id_target, name, original_name, description, notes, resource_url FROM public.get_targets();")
result = cur.fetchall()
tgts = [Target.from_sql_row(row) for row in result]
print(tgts)

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

cur.close()
conn.close()
