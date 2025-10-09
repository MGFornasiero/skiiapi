from typing import Union, List, Dict, Any
import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import APIKeyHeader
import json

from .models import Target # ski.targets , public.get_targets(), public.get_target_info(), public.qry_ts_targets()
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

#####                       NOTE                        #####
#    the connection is set using the env variable SKIURI    #
#############################################################

app = FastAPI()

# --- API Key Security ---
# It's recommended to set this in your environment for production
SECRET_API_KEY = os.environ.get("API_KEY", "bushido_secret_key")
SECRET_ADMIN_API_KEY = os.environ.get("API_ADMINKEY", "bushido_admin_secretkey")

API_KEY_NAME = "BUSHIDO-Key"
ADMIN_API_KEY_NAME = "BUSHIDO-AdminKey"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)
api_admin_key_header = APIKeyHeader(name=ADMIN_API_KEY_NAME, auto_error=True)

async def get_api_key(api_key: str = Depends(api_key_header)):
    """
    Dependency that checks for the presence and validity of an API key in the request header.
    """
    if api_key == SECRET_API_KEY or api_key == SECRET_ADMIN_API_KEY:
        return api_key
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
            headers={"WWW-Authenticate": "API-Key"},
        )
async def get_admin_api_key(api_key: str = Depends(api_admin_key_header)):
    """
    Dependency that checks for the presence and validity of an andmin API key in the request header.
    """
    if api_key != SECRET_ADMIN_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
            headers={"WWW-Authenticate": "API-Key"},
        )
    return api_key
# --- End API Key Security ---


import psycopg2
import psycopg2.pool

uri = os.environ['SKIURI']
admin_uri = os.environ['SKIURI'] #cambiare la variabile per un utente diverso

pool = psycopg2.pool.SimpleConnectionPool(
    1, 5, uri
)


@app.get("/")
def read_root():
    """Returns a welcome message."""
    return {"Hello": "Karate!!!"}

@app.get("/grade_id/{gradetype}/{grade}")
def read_gradeid(gradetype:str ,grade: int):
    """Retrieves the ID for a given grade and grade type."""
    query = f"SELECT get_gradeid({grade},'{gradetype}');" 
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            result = cur.fetchone()
    finally:
        pool.putconn(conn)

    grade_id = int(result[0])
    return {"grade": grade_id,}

@app.get("/numberofkihon/{grade_id}")
def read_kihonsequencedomain(grade_id: int ):
    """Retrieves the number of kihon sequences for a given grade ID."""
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT public.get_nkihon(%s);", (grade_id,))
            result = cur.fetchone()
    finally:
        pool.putconn(conn)
    max_seq = int(result[0])
    return {"grade": grade_id,"n_kihon":max_seq}

@app.get("/kihon_list/{grade_id}/{sequenza}")
def kihon_dtls(grade_id: int , sequenza: int):
    """Retrieves the details for a specific kihon sequence (sequenza) of a given grade."""
    q_step =f"""
    SELECT id_sequence,
           inventory_id,
           seq_num,
           stand_id,
           technic_id,
           gyaku,
           target_hgt,
           notes,
           resource_url,
           stand_name,
           technic_name
    FROM get_kihon_steps({grade_id}, {sequenza});
    """
    q_tx = f"""
    SELECT id_tx,
           from_sequence,
           to_sequence,
           movement,
           tempo,
           notes,
           resource_url
    FROM get_kihon_tx({grade_id}, {sequenza});
    """
    
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(q_step)
            result_steps = cur.fetchall()
            cur.execute(q_tx)
            result_tx = cur.fetchall()
            cur.execute(f"SELECT get_kihonnotes({grade_id} ,{sequenza});") #da implementare nel json di ritorno
            result_note = cur.fetchone()
            cur.execute(f"SELECT grade,gtype FROM public.get_grade({grade_id});") 
            grade_data = cur.fetchone()
    finally:
        pool.putconn(conn)
    s_results = {
        res[2] : {
            'id_sequence': res[0] ,
            'inventory_id': res[1] ,
            'seq_num': res[2] ,
            'stand': res[3] ,
            'techinc': res[4] ,
            'gyaku': res[5] ,
            'target_hgt': res[6] ,
            'notes': res[7] ,
            'resource_url': res[8] ,
            'stand_name': res[9] ,
            'technic_name': res[10]
        } for res in result_steps
    }
    tx_results = {
        res[0] : {
            'movement': res[3] ,
            'tempo': res[4] ,
            'notes': res[5] ,
            'resource_url': res[6]
        } for res in result_tx
    }
    
    tx_mapping_to = {
        res[2]:res[0] for res in result_tx
    }
    
    tx_mapping_from = {
        res[1]:res[0] for res in result_tx
    }
    
    grade = f"{grade_data[0]}° {grade_data[1]}"
    return {"grade": grade, 
        "grade_id": grade_id, 
        "note": result_note[0], # vedere se funziona ancora il FE
        "sequenza_n":sequenza,
        "tecniche":s_results , 
        "transactions":tx_results ,
        "transactions_mapping_from":tx_mapping_from,
        "transactions_mapping_to":tx_mapping_to
    }

@app.get("/kihons/{grade_id}")
def kihon(grade_id: int):
    """Retrieves all kihon techniques for a given grade ID."""
    query = f"""
    SELECT number,
           seq_num,
           movement,
           technic_id,
           gyaku,
           tecnica,
           stand_id,
           posizione,
           target_hgt,
           notes
    FROM kihon_frmlist({grade_id});
    """
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            result = cur.fetchall()
            cur.execute("SELECT grade, gtype FROM public.get_grade(%s);", (grade_id,))
            grade_data = cur.fetchone()
    finally:
        pool.putconn(conn)
    print(result)
    res = dict()
    for row in result:
        if row[0] not in res.keys(): 
            res[row[0]] = dict()
        res[row[0]][row[1]] = {
            "movement": row[2],
            "technic_id": row[3],
            "gyaku": row[4],
            "tecnica": row[5], 
            "stand_id": row[6],
            "Stand": row[7] ,
            "Target":row[8],
            "Note":row[9]
        }
    
    grade = f"{grade_data[0]}° {grade_data[1]}"
    return {"grade": grade, "grade_id": grade_id, "kihons":res}

@app.get("/kata/{kata_id}")
def kata(kata_id: int):
    """Retrieves the sequence steps and transitions for a given kata ID."""
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                f"SELECT id_sequence, kata_id, seq_num, stand_id, posizione, guardia, facing, Tecniche, embusen, kiai, notes, remarks, resources, resource_url FROM public.get_katasequence({kata_id});"
            )
            steps_result = cur.fetchall()
            cur.execute(
                f"SELECT id_tx, from_sequence, to_sequence, tempo, direction, notes, remarks, resources, resource_url FROM public.get_katatx({kata_id});",
            )
            tx_result = cur.fetchall()
            cur.execute(f"SELECT kata, serie, starting_leg, notes, remarks, resources, resource_url FROM public.get_katainfo({kata_id});")
            info = cur.fetchone()

            cur.execute(f"SELECT id_bunkai,version,name,description,notes,resources FROM public.get_katabunkais({kata_id});") #id_bunkai,version,name,description,notes,resources
            bunkais_result = cur.fetchall()
            bunkai_ids  = {
                res[0]:{"version":res[1],"name":res[2],"description":res[3],"notes":res[4],"resources":res[5]} for res in bunkais_result
            }
    finally:
        pool.putconn(conn)

    res_steps = {
        step[2]: {
            'id_sequence': step[0],
            'kata_id': step[1],
            'seq_num': step[2],
            'stand_id': step[3],
            'posizione': step[4],
            'guardia': step[5],
            'facing': step[6],
            'tecniche': step[7],
            'embusen': step[8],
            'kiai': step[9],
            'notes': step[10],
            'remarks': step[11],
            'resources': step[12],
            'resource_url': step[13]
        } for step in steps_result
    }

    transaction = {
        res[0]: {
            "tempo": res[3],
            "direction": res[4],
            "note": res[5],
            "remarks": res[6],
            "resources": res[7],
            "resource_url": res[8]
        } for res in tx_result
    }

    tx_mapping_to = {
        res[2]: res[0] for res in tx_result
    }

    tx_mapping_from = {
        res[1]: res[0] for res in tx_result
    }

    return {
        "kata_id": kata_id,
        "kata_name": info[0],
        "serie": info[1],
        "Gamba": info[2],
        "notes": info[3],
        "remarks": info[4],
        "resources": info[5],
        "resource_url": info[6],
        "steps": res_steps,
        "transactions": transaction,
        "transactions_mapping_from": tx_mapping_from,
        "transactions_mapping_to": tx_mapping_to,
        "bunkai_ids": bunkai_ids
    }
@app.get("/bunkai_inventory/{kata_id}")
def bunkai_inventory(kata_id: int): #err
    """Retrieves the inventory of all bunkais for a given kata ID."""
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(f"SELECT id_bunkai, kata_id, version, name, description, notes,resources, resource_url FROM public.get_katabunkais({kata_id});")
            bunkai_result = cur.fetchall()
    finally:
        pool.putconn(conn)
    print(bunkai_result)
    bunkai_inventory = {res[0]:{
        'kata_id': res[1],
        'version': res[2],
        'name': res[3],
        'description': res[4],
        'notes': res[5],
        'resources': json.loads(str(res[6])) if res[6] else {},
        'resource_url': res[7]
    } for res in bunkai_result}
    return {"kata_id": kata_id, "bunkai_inventory": bunkai_inventory}

@app.get("/bunkai_dtls/{bunkai_id}")
def bunkaisteps(bunkai_id: int):
    """Retrieves the sequence steps for a given bunkai ID."""  
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(f"SELECT id_bunkaisequence, bunkai_id, kata_sequence_id, description, notes, array_to_json(remarks) as remarks, resources, resource_url FROM public.get_bunkai({bunkai_id});")
            steps_result = cur.fetchall()
    finally:
        pool.putconn(conn)
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
    return {"bunkai_id": bunkai_id, "bunkai_steps": res_steps}

@app.get("/grade_inventory")
def grade_inventory():
    """Retrieves the inventory of all available grades."""
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT grade, gtype, id_grade FROM public.show_gradeinventory();")
            results = cur.fetchall()
    finally:
        pool.putconn(conn)
    gradi = {res[2]:f"{res[0]}° {res[1]}" for res in results}
    return {"gradi": str(gradi)}

@app.get("/kata_inventory")
def kata_inventory():
    """Retrieves the inventory of all available katas."""
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id_kata, kata, serie, starting_leg, notes, remarks, resources, resource_url FROM public.show_katainventory();")
            results = cur.fetchall()
    finally:
        pool.putconn(conn)
    kata = {res[1]:res[0] for res in results}
    return {"kata": kata}

@app.get("/info_technic/{item_id}") 
def get_info_technic(item_id: int):
    """Retrieves information about a specific technic by its ID."""
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(f"SELECT id_technic, waza, name, description, notes, resource_url FROM public.get_technic_info({item_id});")
            result = cur.fetchone()
    finally:
        pool.putconn(conn)
    if result:
        row = {'id_technic':result[0], 'waza':result[1], 'name':result[2], 'description':result[3], 'notes':result[4], 'resource_url':result[5]}
    else:
        row = {'id_technic':None, 'waza':None, 'name':None, 'description':None, 'notes':None, 'resource_url':None}
    return {"id":item_id,"info_technic":row}

@app.get("/technics_decomposition/{item_id}")
def get_technic_decomposition(item_id: int): #err
    """Retrieves the decomposition of a specific technic by its ID."""
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(f"SELECT step_num, stand_id, technic_id, gyaku, target_hgt, notes, resource_url FROM get_technic_decomposition({item_id});")
            results = cur.fetchall()
    finally:
        pool.putconn(conn)
    output = {
        result[0]:{
            'step_num':result[0], 
            'stand_id':result[1], 
            'technic_id':result[2], 
            'gyaku':result[3], 
            'target_hgt':result[4], 
            'notes':result[5], 
            'resource_url':result[6]
        } for result in results}
    if results:
        return {"id":item_id,"technic_decomposition":output}
    else:
        return {"id":item_id,"technic_decomposition":[]}

@app.get("/info_stand/{item_id}")
def get_info_stand(item_id: int):
    """Retrieves information about a specific stand (position) by its ID."""
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(f"SELECT id_stand, name, description, illustration_url, notes FROM get_stand_info({item_id});")
            result = cur.fetchone()
    finally:
        pool.putconn(conn)
    if result:
        row =  {'id_stand':result[0], 'name':result[1], 'description':result[2], 'illustration_url':result[3], 'notes':result[4]}
    else:
        row =  {'id_stand':None, 'name':None, 'description':None, 'illustration_url':None, 'notes':None}
    return {"id":item_id,"info_stand":row}


@app.get("/info_strikingparts/{item_id}")
def get_info_strikingparts(item_id: int):
    """Retrieves information about a specific striking part by its ID."""
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(f"SELECT id_part, name, translation, description, notes, resource_url FROM get_strikingparts_info({item_id});")
            result = cur.fetchone()
    finally:
        pool.putconn(conn)
    print(result)
    if result:
        row =  {'id_part':result[0], 'name':result[1], 'translation':result[2], 'description':result[3], 'notes':result[4], 'resource_url':result[5]}
    else:
        row =  {'id_part':None, 'name':None, 'translation':None, 'description':None, 'notes':None, 'resource_url':None}
    return {"id":item_id,"info_strikingparts":row}


@app.get("/info_target/{item_id}")
def get_info_target(item_id: int):
    """Retrieves information about a specific target by its ID."""
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(f"SELECT id_target, name, original_name, description, notes, resource_url FROM get_target_info({item_id});")
            result = cur.fetchone()
    finally:
        pool.putconn(conn)
    if result:
        row =  {'id_target':result[0], 'name':result[1], 'original_name':result[2], 'description':result[3], 'notes':result[4], 'resource_url':result[5]}
    else:
        row =  {'id_target':None, 'name':None, 'original_name':None, 'description':None, 'notes':None, 'resource_url':None}
    return {"id":item_id,"info_target":row}


@app.get("/finder")
def finder(search: str = ""):
    """Performs a full-text search across targets, technics, stands, and striking parts."""
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT pertinenza, pertinenza_relativa, id_target, name, original_name, description, notes, resource_url FROM public.qry_ts_targets(%s);", (search,))
            results_targets = cur.fetchall()

            cur.execute("SELECT pertinenza, pertinenza_relativa, id_technic, waza, name, description, notes, resource_url FROM public.qry_ts_technics(%s);", (search,))
            results_technics = cur.fetchall()

            cur.execute("SELECT pertinenza, pertinenza_relativa, id_stand, name, description, illustration_url, notes FROM public.qry_ts_stands(%s);", (search,))
            results_stands = cur.fetchall()

            cur.execute("SELECT pertinenza, pertinenza_relativa, id_part, name, translation, description, notes, resource_url FROM public.qry_ts_strikingparts(%s);", (search,))
            results_strikingparts = cur.fetchall() 
    finally:
        pool.putconn(conn)

    # Build parsed dictionaries like /finder
    output_technics = {
        r[2]: {
            'id_technic': r[2],
            'waza': r[3],
            'name': r[4],
            'description': r[5],
            'notes': r[6],
            'resource_url': r[7]
        } for r in results_technics
    }

    output_stands = {
        r[2]: {
            'id_stand': r[2],
            'name': r[3],
            'description': r[4],
            'illustration_url': r[5],
            'notes': r[6]
        } for r in results_stands
    }

    output_strikingparts = {
        r[2]: {
            'id_part': r[2],
            'name': r[3],
            'translation': r[4],
            'description': r[5],
            'notes': r[6],
            'resource_url': r[7]
        } for r in results_strikingparts
    }

    output_targets = {
        r[2]: {
            'id_target': r[2],
            'name': r[3],
            'original_name': r[4],
            'description': r[5],
            'notes': r[6],
            'resource_url': r[7]
        } for r in results_targets
    }

    maxrel = max(
        [r[0] for r in results_targets] +
        [r[0] for r in results_technics] +
        [r[0] for r in results_stands] +
        [r[0] for r in results_strikingparts]
    ) if (results_targets or results_technics or results_stands or results_strikingparts) else 1

    relevance_results_targets = {r[2]: {"abs_relevance": r[0], "relative_relevance": r[0]/maxrel} for r in results_targets}
    relevance_results_technics = {r[2]: {"abs_relevance": r[0], "relative_relevance": r[0]/maxrel} for r in results_technics}
    relevance_results_stands = {r[2]: {"abs_relevance": r[0], "relative_relevance": r[0]/maxrel} for r in results_stands}
    relevance_results_strikingparts = {r[2]: {"abs_relevance": r[0], "relative_relevance": r[0]/maxrel} for r in results_strikingparts}

    return {
        "ts": search,
        "max_relevance": maxrel,
        "Targets_relevance": relevance_results_targets,
        "Technics_relevance": relevance_results_technics,
        "Stands_relevance": relevance_results_stands,
        "Striking_parts_relevance": relevance_results_strikingparts,
        "Targets": output_targets,
        "Technics": output_technics,
        "Stands": output_stands,
        "Striking_parts": output_strikingparts
    }



@app.get("/technic_inventory")
def info_technic_inventory():
    """Retrieves the inventory of all technics."""
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id_technic, waza, name, description, notes, resource_url FROM public.get_technics();")
            results = cur.fetchall()
    finally:
        pool.putconn(conn)
    output = {
            result[0]:{
                'id_technic':result[0], 
                 'waza':result[1], 
                 'name':result[2], 
                 'description':result[3], 
                 'notes':result[4], 
                 'resource_url':result[5]
                }
            for result in results}
    if results:
        return {"technics_inventory":output}
    else:
        return {"technics_inventory":[]}


@app.get("/stand_inventory")
def get_stand_inventory():
    """Retrieves the inventory of all stands."""
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id_stand, name, description, illustration_url, notes FROM public.get_stands();")
            results = cur.fetchall()
    finally:
        pool.putconn(conn)
    output = {
        result[0]:{
            'id_stand':result[0], 
            'name':result[1], 
            'description':result[2], 
            'illustration_url':result[3], 
            'notes':result[4]
        } for result in results}
    if results:
        return {"stands_inventory":output}
    else:
        return {"stands_inventory":[]}


@app.get("/strikingparts_inventory")
def get_strikingparts_inventory():
    """Retrieves the inventory of all striking parts."""
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id_part, name, translation, description, notes, resource_url FROM public.get_strikingparts();")
            results = cur.fetchall()
    finally:
        pool.putconn(conn)
    output = {result[0]:{
            'id_part':result[0], 
            'name':result[1], 
            'translation':result[2], 
            'description':result[3], 
            'notes':result[4], 
            'resource_url':result[5]}
            for result in results}
    if results:
        return {"strikingparts_inventory":output}
    else:
        return {"strikingparts_inventory":[]}


@app.get("/target_inventory")
def get_target_inventory():
    """Retrieves the inventory of all targets."""
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id_target, name, original_name, description, notes, resource_url FROM public.get_targets();")
            results = cur.fetchall()
    finally:
        pool.putconn(conn)
    output = {result[0]:{
            'id_target':result[0], 
            'name':result[1], 
            'original_name':result[2], 
            'description':result[3], 
            'notes':result[4], 
            'resource_url':result[5]
        } for result in results}
    if results: 
        return {"targets_inventory":output}
    else:
        return {"targets_inventory":[]}
    

@app.get("/utils/present_kata/{kata_id}")  
def present_kata(kata_id: int):
    """Checks if a kata with the given ID exists in the database."""
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM public.info_kata({kata_id});")
            result = cur.fetchall()
    finally:
        pool.putconn(conn)

    present = {res[0]:{
        "id_sequence" :  res[0],
        "kata_id" :  res[1],
        "seq_num" :  res[2],
        "stand_id" :  res[3],
        "stand_name" :  res[4],
        "speed" :  res[5],
        "side" :  res[6],
        "hips" :  res[7],
        "embusen" :  res[8],
        "facing" :  res[9],
        "kiai" :  res[10],
        "notes" :  res[11],
        "Tecniche" :  res[12]
    } for res in result}
    return {"info": present}


@app.get("/secure/", dependencies=[Depends(get_admin_api_key)])
def get_secure_data():
    """
    An example of a route secured with an API key.
    Only requests with a valid `BUSHIDO-Key` header will be able to access this.
    """
    return {"data": "This is secure data, accessible only with a valid API key."}



# --- POST: Insert Target ---

@app.put("/admin/insert/targets/bulk", status_code=201)
def create_targets_bulk(targets: List[Target], api_key: str = Depends(get_admin_api_key)): #blocco di record
    """
    Inserts multiple Target rows in a single transaction.
    """
    conn = psycopg2.connect(admin_uri)
    cur = conn.cursor()
    print(targets)
    values = ",".join([t.to_sql_values() for t in targets])
    col_list=[f for f in Target.model_fields]
    columns = ", ".join(col_list)
    upsertspecification = ", ".join([f"{col}=EXCLUDED.{col}" for col in col_list])
    print(values)
    print(columns)
    upsertquery = f"""INSERT INTO ski.targets({columns})
    VALUES {values}
        ON CONFLICT (id_target)
        DO UPDATE SET {upsertspecification}
      RETURNING {columns};
    """
    print(upsertquery)
    try:
        cur.execute(upsertquery)
        conn.commit()
        res_targets = cur.fetchall()
        targets = [
            Target(
                id_target=row[0],
                name=row[1],
                original_name=row[2],
                description=row[3],
                notes=row[4],
                resource_url=row[5],
            )
            for row in res_targets
        ]
        return {"message": "Inserted", 
                "target": targets
        }

    except psycopg2.Error as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Database error: {e.pgerror}")
    finally:
        cur.close()
        conn.close()
@app.put("/admin/delete/targets/bulk", status_code=201)

def delete_targets_bulk(ids: List[int], api_key: str = Depends(get_admin_api_key)):
    conn = psycopg2.connect(admin_uri)
    cur = conn.cursor()
    print(ids)
    values = ",".join([f"( {i} )" for i in ids])
    col_list=[f for f in Target.model_fields]
    columns = ", ".join(col_list)
    # upsertspecification = ", ".join([f"{col}=EXCLUDED.{col}" for col in col_list])
    print(values)
    # print(columns)
    deletequery = f"""
    WITH to_delete AS (
        SELECT unnest(ARRAY[{','.join(map(str, ids))}]) AS ids
    )
    DELETE FROM ski.targets
    WHERE id_target IN (SELECT ids FROM to_delete)
    RETURNING {columns};
    """
    print(deletequery)
    try:
        cur.execute(deletequery)
        conn.commit()
        res_targets = cur.fetchall()
        print(res_targets)
        targets = [
            Target(
                id_target=row[0],
                name=row[1],
                original_name=row[2],
                description=row[3],
                notes=row[4],
                resource_url=row[5],
            )
            for row in res_targets
        ]
        return {"message": "Deleted", 
                "target": targets
        }

    except psycopg2.Error as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Database error: {e.pgerror}")
    finally:
        cur.close()
        conn.close()

@app.get("/admin/select/targets/all", dependencies=[Depends(get_admin_api_key)])
def select_targets():
    """
    """
    conn = psycopg2.connect(admin_uri)
    cur = conn.cursor()
    cur.execute("SELECT id_target,name,original_name,description,notes,resource_url FROM ski.targets;")
    res_targets = cur.fetchall()
    cur.close()
    conn.close()
    targets = [
        Target(
            id_target=row[0],
            name=row[1],
            original_name=row[2],
            description=row[3],
            notes=row[4],
            resource_url=row[5],
        )
        for row in res_targets
    ]
    return {"message": "Target content", 
            "target": targets
    }

#StrikingPart Technic Stand Grade