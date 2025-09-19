from typing import Union
import os
from fastapi import FastAPI

#####                       NOTE                        #####
#    the connection is set using the env variable SKIURI    #
#############################################################

app = FastAPI()

import psycopg2
uri = os.environ['SKIURI']
print(uri)

@app.get("/")
def read_root():
    """Returns a welcome message."""
    return {"Hello": "Karate!!!"}

@app.get("/grade_id/{gradetype}/{grade}")
def read_gradeid(gradetype:str ,grade: int):
    """Retrieves the ID for a given grade and grade type."""
    query = f"SELECT get_gradeid({grade},'{gradetype}');" 
    conn = psycopg2.connect(uri)
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchone()
    cur.close()
    conn.close()
    grade_id = int(result[0])
    return {"grade": grade_id,}

@app.get("/numberofkihon/{grade_id}")
def read_kihonsequencedomain(grade_id: int ):
    """Retrieves the number of kihon sequences for a given grade ID."""
    conn = psycopg2.connect(uri)
    cur = conn.cursor()
    cur.execute("SELECT public.get_nkihon(%s);", (grade_id,))

    result = cur.fetchone()
    cur.close()
    conn.close()
    print(result)
    max_seq = int(result[0])
    print(max_seq)
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
    
    conn = psycopg2.connect(uri)
    cur = conn.cursor()
    cur.execute(q_step)
    result_steps = cur.fetchall()
    cur.execute(q_tx)
    result_tx = cur.fetchall()
    cur.execute(f"SELECT get_kihonnotes({grade_id} ,{sequenza});") #da implementare nel json di ritorno
    result_note = cur.fetchone()
    cur.execute(f"SELECT grade,gtype FROM public.get_grade({grade_id});") 
    grade_data = cur.fetchone()
    cur.close()
    conn.close()
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
    conn = psycopg2.connect(uri)
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    cur.execute("SELECT grade, gtype FROM public.get_grade(%s);", (grade_id,))

    grade_data = cur.fetchone()
    cur.close()
    conn.close()
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
    conn = psycopg2.connect(uri)
    cur = conn.cursor()
    cur.execute(
        "SELECT id_sequence, kata_id, seq_num, stand_id, posizione, guardia, facing, Tecniche, embusen, kiai, notes, remarks, resources, resource_url FROM public.get_katasequence(%s);",
        (kata_id,)
    )
    steps_result = cur.fetchall()
    cur.execute(
        "SELECT id_tx, from_sequence, to_sequence, tempo, direction, notes, remarks, resources, resource_url FROM public.get_katatx(%s);",
        (kata_id,)
    )
    tx_result = cur.fetchall()
    cur.execute("SELECT kata, serie, starting_leg, notes, remarks, resources, resource_url FROM public.get_katainfo(%s);", (kata_id,))
    info = cur.fetchone()
    cur.execute("SELECT id_bunkaisequence, bunkai_id, kata_sequence_id, description, notes, resource_url FROM public.get_bunkais(%s);", (kata_id,))
    bunkai_result = cur.fetchall()
    print(bunkai_result)

    cur.close()
    conn.close()

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
        "transactions_mapping_to": tx_mapping_to
    }

@app.get("/grade_inventory")
def grade_inventory():
    """Retrieves the inventory of all available grades."""
    conn = psycopg2.connect(uri)
    cur = conn.cursor()
    cur.execute("SELECT grade, gtype, id_grade FROM public.show_gradeinventory();")

    results = cur.fetchall()
    cur.close()
    conn.close()
    gradi = {res[2]:f"{res[0]}° {res[1]}" for res in results}
    return {"gradi": str(gradi)}

@app.get("/kata_inventory")
def kata_inventory():
    """Retrieves the inventory of all available katas."""
    conn = psycopg2.connect(uri)
    cur = conn.cursor()
    cur.execute("SELECT id_kata, kata, serie, starting_leg, notes, remarks, resources, resource_url FROM public.show_katainventory();")
    results = cur.fetchall()
    cur.close()
    conn.close()
    kata = {res[1]:res[0] for res in results}
    return {"kata": kata}

@app.get("/info_technic/{item_id}") 
def get_info_technic(item_id: int):
    """Retrieves information about a specific technic by its ID."""
    conn = psycopg2.connect(uri)
    cur = conn.cursor()
    cur.execute(f"SELECT id_technic, waza, name, description, notes, resource_url FROM public.get_technic_info({item_id});")
    result = cur.fetchone()
    cur.close()
    conn.close()
    if result:
        row = {'id_technic':result[0], 'waza':result[1], 'name':result[2], 'description':result[3], 'notes':result[4], 'resource_url':result[5]}
    else:
        row = {'id_technic':None, 'waza':None, 'name':None, 'description':None, 'notes':None, 'resource_url':None}
    return {"id":item_id,"info_technic":row}

@app.get("/technics_decomposition/{item_id}")
def get_technic_decomposition(item_id: int):
    """Retrieves the decomposition of a specific technic by its ID."""
    conn = psycopg2.connect(uri)
    cur = conn.cursor()
    cur.execute(f"SELECT step_num, stand_id, technic_id, gyaku, target_hgt, notes, resource_url FROM get_technic_decomposition({item_id});")
    results = cur.fetchall()
    cur.close()
    conn.close()
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
    conn = psycopg2.connect(uri)
    cur = conn.cursor()
    cur.execute(f"SELECT id_stand, name, description, illustration_url, notes FROM get_stand_info({item_id});")
    result = cur.fetchone()
    cur.close()
    conn.close()
    if result:
        row =  {'id_stand':result[0], 'name':result[1], 'description':result[2], 'illustration_url':result[3], 'notes':result[4]}
    else:
        row =  {'id_stand':None, 'name':None, 'description':None, 'illustration_url':None, 'notes':None}
    return {"id":item_id,"info_stand":row}


@app.get("/info_strikingparts/{item_id}")
def get_info_strikingparts(item_id: int):
    """Retrieves information about a specific striking part by its ID."""
    conn = psycopg2.connect(uri)
    cur = conn.cursor()
    cur.execute(f"SELECT id_part, name, translation, description, notes, resource_url FROM get_strikingparts_info({item_id});")
    result = cur.fetchone()
    cur.close()
    conn.close()
    print(result)
    if result:
        row =  {'id_part':result[0], 'name':result[1], 'translation':result[2], 'description':result[3], 'notes':result[4], 'resource_url':result[5]}
    else:
        row =  {'id_part':None, 'name':None, 'translation':None, 'description':None, 'notes':None, 'resource_url':None}
    return {"id":item_id,"info_strikingparts":row}


@app.get("/info_target/{item_id}")
def get_info_target(item_id: int):
    """Retrieves information about a specific target by its ID."""
    conn = psycopg2.connect(uri)
    cur = conn.cursor()
    cur.execute(f"SELECT id_target, name, original_name, description, notes, resource_url FROM get_target_info({item_id});")
    result = cur.fetchone()
    cur.close()
    conn.close()
    if result:
        row =  {'id_target':result[0], 'name':result[1], 'original_name':result[2], 'description':result[3], 'notes':result[4], 'resource_url':result[5]}
    else:
        row =  {'id_target':None, 'name':None, 'original_name':None, 'description':None, 'notes':None, 'resource_url':None}
    return {"id":item_id,"info_target":row}


@app.get("/finder")
def finder(search: str = ""):
    """Performs a full-text search across targets, technics, stands, and striking parts."""
    conn = psycopg2.connect(uri)
    cur = conn.cursor()

    # Use database functions instead of inline queries
    cur.execute("SELECT pertinenza, pertinenza_relativa, id_target, name, original_name, description, notes, resource_url FROM public.qry_ts_targets(%s);", (search,))
    results_targets = cur.fetchall()

    cur.execute("SELECT pertinenza, pertinenza_relativa, id_technic, waza, name, description, notes, resource_url FROM public.qry_ts_technics(%s);", (search,))
    results_technics = cur.fetchall()

    cur.execute("SELECT pertinenza, pertinenza_relativa, id_stand, name, description, illustration_url, notes FROM public.qry_ts_stands(%s);", (search,))
    results_stands = cur.fetchall()

    cur.execute("SELECT pertinenza, pertinenza_relativa, id_part, name, translation, description, notes, resource_url FROM public.qry_ts_strikingparts(%s);", (search,))
    results_strikingparts = cur.fetchall()

    cur.close()
    conn.close()

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
    conn = psycopg2.connect(uri)
    cur = conn.cursor()
    cur.execute("SELECT id_technic, waza, name, description, notes, resource_url FROM public.get_technics();")
    results = cur.fetchall()
    cur.close()
    conn.close()
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
    conn = psycopg2.connect(uri)
    cur = conn.cursor()
    cur.execute("SELECT id_stand, name, description, illustration_url, notes FROM public.get_stands();")
    results = cur.fetchall()
    cur.close()
    conn.close()
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
    conn = psycopg2.connect(uri)
    cur = conn.cursor()
    cur.execute("SELECT id_part, name, translation, description, notes, resource_url FROM public.get_strikingparts();")
    results = cur.fetchall()
    cur.close()
    conn.close()
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
    conn = psycopg2.connect(uri)
    cur = conn.cursor()
    cur.execute("SELECT id_target, name, original_name, description, notes, resource_url FROM public.get_targets();")
    results = cur.fetchall()
    cur.close()
    conn.close()
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
