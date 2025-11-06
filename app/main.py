from typing import Union, List, Dict, Any
import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import APIKeyHeader
import json

from .models import Target # ski.targets , public.get_targets(), public.get_target_info(), public.qry_ts_targets()
from .models import StrikingPart # ski.strikingparts() , public.get_strikingparts(), public.get_strikingparts_info(), public.qry_ts_strikingparts()
from .models import Stand # ski.stands() , public.get_stands(), public.get_stand_info(), public.qry_ts_stands()
from .models import Technic # ski.technics() , public.get_technics(), public.get_technic_info(), public.qry_ts_technics(), public.get_technic_decomposition()
from .models import Grade # ski.grades() , public.get_grade()
from .models import KihonInventory # ski.kihon_inventory() , public.get_kihons()
from .models import KihonTx #get_kihon_tx()
from .models import KihonStep  #get_kihon_steps()
from .models import KihonFormatted  #kihon_frmlist()
from .models import KataInventory  # ski.kata_inventory() , public.show_katainventory(), public.get_katainfo()
from .models import KataSequenceStep  #get_katasequence()
from .models import KataTx
from .models import BunkaiInventory  # ski.bunkai_inventory() , public.get_katabunkais()
from .models import BunkaiSequence #get_bunkai()

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
import psycopg2.extras

uri = os.environ['SKIURI']
admin_uri = os.environ['SKIURI'] #cambiare la variabile per un utente diverso

pool = psycopg2.pool.SimpleConnectionPool(
    1, 5, uri
)

conn = pool.getconn()
psycopg2.extras.register_composite('embusen_points', conn, globally=True)
psycopg2.extras.register_composite('bodypart', conn, globally=True)
psycopg2.extras.register_composite('detailednotes', conn, globally=True)
pool.putconn(conn)

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
           resources,
           notes,
           tempo,
           resource_url
    FROM get_kihon_tx({grade_id}, {sequenza});
    """
    
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(q_step)
            objs_steps = [KihonStep.from_sql_row(row) for row in cur]
            
            cur.execute(q_tx)
            objs_tx = [KihonTx.from_sql_row(row) for row in cur]
            
            cur.execute(f"SELECT get_kihonnotes({grade_id} ,{sequenza});") #da implementare nel json di ritorno
            result_note = cur.fetchone()
            cur.execute(f"SELECT grade,gtype FROM public.get_grade({grade_id});") 
            grade_data = cur.fetchone()
    finally:
        pool.putconn(conn)

    s_results = {obj.get_id():obj.model_dump() for obj in objs_steps}

    tx_results = {obj.get_id():obj.model_dump() for obj in objs_tx} #quello implmentato sarebbe un subset di colonne
    tx_mapping_to = {obj_tx.get_to():obj_tx.get_id() for obj_tx in objs_tx} 
    
    tx_mapping_from ={obj_tx.get_from():obj_tx.get_id() for obj_tx in objs_tx} 
    
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
            objs = [KihonFormatted.from_sql_row(row) for row in cur]
            cur.execute("SELECT grade, gtype FROM public.get_grade(%s);", (grade_id,))
            grade_data = cur.fetchone()
    finally:
        pool.putconn(conn)
    res = dict()
    for obj in objs:
        num, seq, details = obj.presentation()
        if num not in res.keys(): 
            res[num] = dict()
        res[num][seq] = details
    
    grade = f"{grade_data[0]}° {grade_data[1]}"
    return {"grade": grade, "grade_id": grade_id, "kihons":res}

@app.get("/kata/{kata_id}")
def kata(kata_id: int):
    """Retrieves the sequence steps and transitions for a given kata ID."""
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                f"SELECT id_sequence,kata_id,seq_num,stand_id,posizione,speed,guardia,hips,facing,looking_direction,tecniche,embusen,kiai,notes,remarks,resources,resource_url FROM public.get_katasequence({kata_id});"
            )
            res_cur = cur.fetchall()
            objs_steps = [KataSequenceStep.from_sql_row(row) for row in res_cur]

            cur.execute(
                f"SELECT id_tx, from_sequence, to_sequence, tempo, direction, intermediate_stand_id,looking_direction, notes, remarks, resources, resource_url FROM public.get_katatx({kata_id});",
            )
            res_cur = cur.fetchall()
            objects_tx = [KataTx.from_sql_row(row) for row in res_cur]

            cur.execute(f"SELECT id_kata, kata, serie, starting_leg, notes, resources, resource_url FROM public.get_katainfo({kata_id});")
            info = cur.fetchone()
            objects_info = KataInventory.from_sql_row(info)

            cur.execute(f"SELECT id_bunkai,kata_id,version,name,description,notes,resources,resource_url FROM public.get_katabunkais({kata_id});") #id_bunkai,version,name,description,notes,resources
            objects_bunkai = [BunkaiInventory.from_sql_row(row) for row in cur]

    finally:
        pool.putconn(conn)

    res_steps = {obj.get_id():obj.model_dump() for obj in objs_steps}  

    transaction = {obj.get_id():obj.model_dump() for obj in objects_tx}

    tx_mapping_to = {obj.get_to():obj.get_id() for obj in objects_tx} 

    tx_mapping_from = {obj.get_from():obj.get_id() for obj in objects_tx}

    bunkai_ids  = {obj.get_id():obj.model_dump() for obj in objects_bunkai}
    return {
        "kata_id": kata_id,
        "kata_name": objects_info.kata,
        "serie": objects_info.serie,
        "Gamba": objects_info.starting_leg,
        "notes": objects_info.notes,
        "resources": objects_info.resources,
        "resource_url": objects_info.resource_url,
        "steps": res_steps,
        "transactions": transaction,
        "transactions_mapping_from": tx_mapping_from,
        "transactions_mapping_to": tx_mapping_to,
        "bunkai_ids": bunkai_ids
    }   

@app.get("/bunkai_inventory/{kata_id}")
def bunkai_inventory(kata_id: int):
    """Retrieves the inventory of all bunkais for a given kata ID."""
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(f"SELECT id_bunkai, kata_id, version, name, description, notes,resources, resource_url FROM public.get_katabunkais({kata_id});")
            objs_bunkai = [BunkaiInventory.from_sql_row(row) for row in cur]
    
    finally:
        pool.putconn(conn)
    bunkai_inventory = {obj.get_id():obj.model_dump() for obj in objs_bunkai}
    return {"kata_id": kata_id, "bunkai_inventory": bunkai_inventory}

@app.get("/bunkai_dtls/{bunkai_id}") # da ripensare un pochino il modello dati
def bunkaisteps(bunkai_id: int):
    """Retrieves the sequence steps for a given bunkai ID."""  
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(f"SELECT id_bunkaisequence, bunkai_id, kata_sequence_id, description, notes, array_to_json(remarks) as remarks, resources, resource_url FROM public.get_bunkai({bunkai_id});")
            obj_BunkaiSequence = [BunkaiSequence.from_sql_row(row) for row in cur]
    finally:
        pool.putconn(conn)

    res_steps  = {obj.get_id():obj.model_dump() for obj in obj_BunkaiSequence}
    return {"bunkai_id": bunkai_id, "bunkai_steps": res_steps}

@app.get("/grade_inventory")
def grade_inventory():
    """Retrieves the inventory of all available grades."""
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id_grade, gtype,grade,color FROM public.show_gradeinventory();")
            obj_gredeinv = [Grade.from_sql_row(row) for row in cur]
    finally:
        pool.putconn(conn)

    gradi = {k:v for k,v in (g.presentation() for g in obj_gredeinv)}
    return {"gradi": str(gradi)}

@app.get("/kata_inventory")
def kata_inventory():
    """Retrieves the inventory of all available katas."""
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id_kata, kata, serie, starting_leg, notes, resources, resource_url FROM public.show_katainventory();")
            obj_katainv = [KataInventory.from_sql_row(row) for row in cur]
    finally:
        pool.putconn(conn)
    kata = {k:v for k,v in (k.inventory() for k in obj_katainv)}
    return {"kata": kata}

@app.get("/info_technic/{item_id}") 
def get_info_technic(item_id: int):
    """Retrieves information about a specific technic by its ID."""
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(f"SELECT id_technic, waza, name, description, notes, resource_url FROM public.get_technic_info({item_id});")
            result = cur.fetchone()
            objects_info = Technic.from_sql_row(result)
            print(objects_info)
    finally:
        pool.putconn(conn)
    if result:
        row = objects_info.model_dump()

    else:
        row = {'id_technic':None, 'waza':None, 'name':None, 'description':None, 'notes':None, 'resource_url':None}
    return {"id":item_id,"info_technic":row}

@app.get("/technics_decomposition/{item_id}") # non esistono ancora i modelli della funzione di risposta
def get_technic_decomposition(item_id: int): #da sistemare
    """Retrieves the decomposition of a specific technic by its ID."""
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(f"SELECT step_num, stand_id, technic_id, gyaku, target_hgt, notes, resource_url FROM public.get_technic_decomposition({item_id});")
            results = [row for row in cur]
    finally:
        pool.putconn(conn)
    output = None

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
        row = Stand.from_sql_row(result).model_dump()
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
    if result:
        row =  StrikingPart.from_sql_row(result).model_dump()
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
        row =  Target.from_sql_row(result).model_dump()
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
            results_targets = [row for row in cur]

            cur.execute("SELECT pertinenza, pertinenza_relativa, id_technic, waza, name, description, notes, resource_url FROM public.qry_ts_technics(%s);", (search,))
            results_technics = [row for row in cur]

            cur.execute("SELECT pertinenza, pertinenza_relativa, id_stand, name, description, illustration_url, notes FROM public.qry_ts_stands(%s);", (search,))
            results_stands = [row for row in cur]

            cur.execute("SELECT pertinenza, pertinenza_relativa, id_part, name, translation, description, notes, resource_url FROM public.qry_ts_strikingparts(%s);", (search,))
            results_strikingparts = [row for row in cur] 
    finally:
        pool.putconn(conn)


    objs_technics = [Technic.from_sql_row(row[2:8]) for row in results_technics]
    output_technics = {obj.get_id():obj.model_dump() for obj in objs_technics}
    
    objs_stands = [Stand.from_sql_row(row[2:7]) for row in results_stands]
    output_stands = {obj.get_id():obj.model_dump() for obj in objs_stands}

    objs_strikingparts = [StrikingPart.from_sql_row(row[2:8]) for row in results_strikingparts]
    output_strikingparts = {obj.get_id():obj.model_dump() for obj in objs_strikingparts}

    objs_targets = [Target.from_sql_row(row[2:8]) for row in results_targets]
    output_targets = {obj.get_id():obj.model_dump() for obj in objs_targets}

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
            objs = [Technic.from_sql_row(row) for row in cur]
    finally:
        pool.putconn(conn)

    output = {obj.get_id():obj.model_dump() for obj in objs}
    if output:
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
            objs = [Stand.from_sql_row(row) for row in cur]
    finally:
        pool.putconn(conn)
    output = {obj.get_id():obj.model_dump() for obj in objs}
    if output:
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
            objs = [StrikingPart.from_sql_row(row) for row in cur]
    finally:
        pool.putconn(conn)

    output = {obj.get_id():obj.model_dump() for obj in objs}
    if output:
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
            objs = [Target.from_sql_row(row) for row in cur]
    finally:
        pool.putconn(conn)

    output = {obj.get_id():obj.model_dump() for obj in objs}
    if output: 
        return {"targets_inventory":output}
    else:
        return {"targets_inventory":[]}
    

@app.get("/utils/present_kata/{kata_id}")  # forse da eliminare
def present_kata(kata_id: int):
    """Checks if a kata with the given ID exists in the database."""
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                f"SELECT id_sequence,kata_id,seq_num,stand_id,posizione,speed,guardia,hips,facing,tecniche,embusen,kiai,notes,remarks,resources,resource_url FROM public.get_katasequence({kata_id});"
            )
            objs_steps = [KataSequenceStep.from_sql_row(row) for row in cur]
    finally:
        pool.putconn(conn)

    present = {obj.get_id():obj.model_dump() for obj in objs_steps}
    return {"info": present}


@app.get("/secure/", dependencies=[Depends(get_admin_api_key)])
def get_secure_data():
    """
    An example of a route secured with an API key.
    Only requests with a valid `BUSHIDO-Key` header will be able to access this.
    """
    return {"data": "This is secure data, accessible only with a valid API key."}


