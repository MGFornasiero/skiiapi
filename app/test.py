from typing import Union
import os
import json
import psycopg2
uri = os.environ['SKIURI']
print(uri)

kata_id = 2

conn = psycopg2.connect(uri)
cur = conn.cursor()
cur.execute(f"SELECT id_bunkai, kata_id, version, name, description, notes,resources, resource_url FROM public.get_katabunkais({kata_id});")
bunkai_result = cur.fetchall()
bunkai_inventory = {res[0]:{
    'kata_id': res[1],
    'version': res[2],
    'name': res[3],
    'description': res[4],
    'notes': res[5],
    'resources': json.loads(str(res[6])) if res[6] else {},
    'resource_url': res[7]
} for res in bunkai_result}
print(bunkai_inventory)

bunkai_id = 2

cur.execute(f"SELECT id_bunkaisequence, bunkai_id, kata_sequence_id, description, notes, array_to_json(remarks) as remarks, resources, resource_url FROM public.get_bunkai({bunkai_id});")
steps_result = cur.fetchall()

print(steps_result)
res_steps = {
    step[2]: {
        'id_bunkaisequence': step[0],
        'bunkai_id': step[1],
        'kata_sequence_id': step[2],
        'description': step[3],
        'notes': step[4],
        'remarks': step[5],
        'resources': step[6],
        'resource_url': step[7]
    } for step in steps_result
}
print(res_steps)
cur.close()
conn.close()