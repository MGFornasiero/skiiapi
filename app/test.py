from typing import Union
import os
import json
import sys
import psycopg2
import psycopg2.extras
#../cloud-sql-proxy.exe --address 127.0.0.1 --port 5432 eng-hangar-343507:europe-west12:pg-mgion
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


kata_id = 1



conn = psycopg2.connect(uri)
psycopg2.extras.register_composite('embusen_points', conn, globally=True)
psycopg2.extras.register_composite('bodypart', conn, globally=True)
psycopg2.extras.register_composite('detailednotes', conn, globally=True)

cur = conn.cursor()

cur.execute(
    f"SELECT id_sequence,kata_id,seq_num,stand_id,posizione,speed,guardia,hips,facing,tecniche,embusen,kiai,notes,remarks,resources,resource_url FROM public.get_katasequence({kata_id});"
)
res_cur = cur.fetchall()
#print(res_cur)
for row in res_cur:
    print(row)
    print(KataSequenceStep.from_sql_row(row))
    print("------------------------------------------------------------------------------")

#objs_steps = [KataSequenceStep.from_sql_row(row) for row in res_cur]
#print(objs_steps)

cur.close()
conn.close()
