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
    return {"Hello": "Karate!!!"}

@app.get("/grade_id/{gradetype}/{grade}")
def read_gradeid(gradetype:str ,grade: int):
    """
    da compilare
    """
    query = f"SELECT ski.get_gradeid({grade},'{gradetype}');"
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
    """
    da compilare
    """
    conn = psycopg2.connect(uri)
    cur = conn.cursor()
    cur.execute(f"SELECT MAX(number) FROM ski.kihon_inventory WHERE grade_id = {grade_id} GROUP BY grade_id;")
    result = cur.fetchone()
    cur.close()
    conn.close()
    print(result)
    max_seq = int(result[0])
    print(max_seq)
    return {"grade": grade_id,"n_kihon":max_seq}

@app.get("/kihon_list/{grade_id}/{sequenza}")
def kihon_dtls(grade_id: int , sequenza: int):
    """
    da compilare
    """
    q_step = f"""
    SELECT seq.id_sequence,
        seq.inventory_id,
        seq.seq_num,
        seq.stand,
        seq.techinc,
        seq.gyaku,
        seq.target_hgt,
        seq.notes,
        seq.resource_url,
        stand.name AS stand_name,
        technic.name AS technic_name
    FROM ski.kihon_sequences AS seq
    JOIN ski.kihon_inventory AS inv ON seq.inventory_id = inv.id_inventory
    LEFT JOIN ski.stands as stand ON seq.stand = stand.id_stand
    LEFT JOIN ski.technics as technic ON seq.techinc = technic.id_technic
    WHERE inv.grade_id = {grade_id} and inv.number = {sequenza}
    ORDER BY seq.seq_num;
    """
    q_tx = f"""
    WITH relevant_sequences AS (
        SELECT seq.id_sequence
        FROM ski.kihon_sequences AS seq
        JOIN ski.kihon_inventory AS inv ON seq.inventory_id = inv.id_inventory
        WHERE inv.grade_id = {grade_id} and inv.number = {sequenza}
    )
    SELECT tx.id_tx,
        tx.from_seq,
        tx.to_seq,
        tx.movement,
        tx.tempo,
        tx.notes,
        tx.resource_url
    FROM ski.kihon_tx AS tx
    WHERE tx.from_seq IN (SELECT id_sequence FROM relevant_sequences)
       OR tx.to_seq IN (SELECT id_sequence FROM relevant_sequences)
    ORDER BY tx.from_seq;
    """
    
    conn = psycopg2.connect(uri)
    cur = conn.cursor()
    cur.execute(q_step)
    result_steps = cur.fetchall()
    cur.execute(q_tx)
    result_tx = cur.fetchall()
    cur.execute(f"SELECT notes FROM ski.kihon_inventory WHERE grade_id = {grade_id} and number = {sequenza};")
    result_note = cur.fetchone()
    cur.execute(f"SELECT grade,gtype FROM ski.grades WHERE id_grade = {grade_id};")
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
        "sequenza_n":sequenza,
        "tecniche":s_results , 
        "transactions":tx_results ,
        "transactions_mapping_from":tx_mapping_from,
        "transactions_mapping_to":tx_mapping_to
    }

@app.get("/kihons/{grade_id}")
def kihon(grade_id: int):
    """
    da compilare
    """
    query = f"""
    SELECT 
        inv.number ,
        seq.seq_num,
        tx.movement ,
        CASE
             WHEN seq.gyaku THEN CONCAT('(Gyaku) ',tech.name)
             ELSE tech.name
        END AS tecnica,
        stands.name AS posizione ,
        seq.target_hgt,
        seq.notes
    FROM ski.kihon_sequences AS seq
    INNER JOIN ski.kihon_inventory AS inv
    ON seq.inventory_id = inv.id_inventory
    LEFT JOIN ski.kihon_tx AS tx 
    ON seq.id_sequence = tx.to_seq 
    LEFT JOIN ski.technics AS tech
    ON seq.techinc = tech.id_technic
    LEFT JOIN ski.stands as stands
    ON seq.stand = stands.id_stand
    WHERE inv.grade_id = {grade_id}
    AND seq_num != 0
    ORDER BY inv.number,seq_num;
    """
    conn = psycopg2.connect(uri)
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    cur.execute(f"SELECT grade,gtype FROM ski.grades WHERE id_grade = {grade_id};")
    grade_data = cur.fetchone()
    cur.close()
    conn.close()
    print(result)
    res = dict()
    for row in result:
        if row[0] not in res.keys(): 
            res[row[0]] = dict()
        res[row[0]][row[1]] = {"movement": row[2],"tecnica": row[3], "Stand": row[4] ,"Target":row[5],"Note":row[6]}
    
    grade = f"{grade_data[0]}° {grade_data[1]}"
    return {"grade": grade, "grade_id": grade_id, "kihons":res}

@app.get("/kata/{kata_id}")
def kata(kata_id: int):
    """
    da compilare
    """
    conn = psycopg2.connect(uri)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM ski.get_katasequence({kata_id});")
    steps_result = cur.fetchall()
    cur.execute(f"SELECT * FROM ski.get_katatx({kata_id});")
    tx_result = cur.fetchall()
    cur.execute(f"SELECT kata , serie ,starting_leg FROM ski.Kata_inventory Where id_kata = {kata_id};")
    info = cur.fetchone()
    cur.close()
    conn.close()
   
    res_steps = {
        step[2]:{
            'id_sequence' : step[0] , 
            'kata_id' : step[1] , 
            'seq_num' : step[2] , 
            'stand_id' : step[3] , 
            'posizione' : step[4] , 
            'guardia' : step[5] , 
            'facing' : step[6] , 
            'tecniche' : step[7] , 
            'embusen' : step[8] , 
            'kiai' : step[9]
        } for step in  steps_result
    }
    
    transaction = {
        res[0]:{
            "tempo":res[3],
            "direction":res[4]
        } for res in tx_result
    }
    
    tx_mapping_to = {
        res[2]:res[0] for res in tx_result
    }
    
    tx_mapping_from = {
        res[1]:res[0] for res in tx_result
    }
    
    return {
        "kata_id": kata_id,
        "kata_name":info[0],
        "serie":info[1], 
        "Gamba":info[2], 
        "steps":res_steps , 
        "transactions":transaction ,
        "transactions_mapping_from":tx_mapping_from,
        "transactions_mapping_to":tx_mapping_to
    }


@app.get("/grade_inventory")
def grade_inventory():
    conn = psycopg2.connect(uri)
    cur = conn.cursor()
    cur.execute("SELECT grade,gtype, id_grade FROM ski.grades;")
    results = cur.fetchall()
    cur.close()
    conn.close()
    gradi = {res[2]:f"{res[0]}° {res[1]}" for res in results}
    return {"gradi": str(gradi)}

@app.get("/kata_inventory")
def kata_inventory():
    conn = psycopg2.connect(uri)
    cur = conn.cursor()
    cur.execute("SELECT  id_kata , kata ,serie , starting_leg , notes , resource_url FROM ski.Kata_inventory;")
    results = cur.fetchall()
    cur.close()
    conn.close()
    kata = {res[1]:res[0] for res in results}
    return {"kata": kata}

@app.get("/info_technic/{item_id}")
def get_info_technic(item_id: int):
    conn = psycopg2.connect(uri)
    cur = conn.cursor()
    cur.execute(f"SELECT id_technic, waza, name, description, notes, resource_url FROM ski.get_technic_info({item_id});")
    result = cur.fetchone()
    cur.close()
    conn.close()
    if result:
        return {'id_technic':result[0], 'waza':result[1], 'name':result[2], 'description':result[3], 'notes':result[4], 'resource_url':result[5]}
    else:
        return {'id_technic':None, 'waza':None, 'name':None, 'description':None, 'notes':None, 'resource_url':None}


@app.get("/info_stand/{item_id}")
def get_info_stand(item_id: int):
    conn = psycopg2.connect(uri)
    cur = conn.cursor()
    cur.execute(f"SELECT id_stand, name, description, illustration_url, notes FROM ski.get_stand_info({item_id});")
    result = cur.fetchone()
    cur.close()
    conn.close()
    if result:
        return {'id_stand':result[0], 'name':result[1], 'description':result[2], 'illustration_url':result[3], 'notes':result[4]}
    else:
        return {'id_stand':None, 'name':None, 'description':None, 'illustration_url':None, 'notes':None}


@app.get("/info_strikingparts/{item_id}")
def get_info_strikingparts(item_id: int):
    conn = psycopg2.connect(uri)
    cur = conn.cursor()
    cur.execute(f"SELECT id_part, name, translation, description, notes, resource_url FROM ski.get_strikingparts_info({item_id});")
    result = cur.fetchone()
    cur.close()
    conn.close()
    print(result)
    if result:
        return {'id_part':result[0], 'name':result[1], 'translation':result[2], 'description':result[3], 'notes':result[4], 'resource_url':result[5]}
    else:
        return {'id_part':None, 'name':None, 'translation':None, 'description':None, 'notes':None, 'resource_url':None}


@app.get("/info_target/{item_id}")
def get_info_target(item_id: int):
    conn = psycopg2.connect(uri)
    cur = conn.cursor()
    cur.execute(f"SELECT id_target, name, original_name, description, notes, resource_url FROM ski.get_target_info({item_id});")
    result = cur.fetchone()
    cur.close()
    conn.close()
    if result:
        return {'id_target':result[0], 'name':result[1], 'original_name':result[2], 'description':result[3], 'notes':result[4], 'resource_url':result[5]}
    else:
        return {'id_target':None, 'name':None, 'original_name':None, 'description':None, 'notes':None, 'resource_url':None}


@app.get("/finder")
def finder(search:str = ""):
    """
    segnaposto per l'endpoint ma decidere meglio l'implementazione
    """
    query_targets = f"""
    WITH ts AS (
        SELECT id,
            ski.ts_normalizer(name_rank,description_rank,notes_rank) AS pertinenza
        FROM ski.get_ts_targets($ts${search}$ts$)
        ORDER BY pertinenza
    )
    SELECT ts.pertinenza ,
    ts.pertinenza / (SELECT MAX(pertinenza) FROM ts ) AS pertinenza_relativa ,
        tbl.*
    FROM ts
    INNER JOIN ski.targets AS tbl
    ON ts.id = tbl.id_target;
    """
    query_technics = f"""
    WITH ts AS (
        SELECT id,
            ski.ts_normalizer(name_rank,description_rank,notes_rank) AS pertinenza
        FROM ski.get_ts_technics($ts${search}$ts$)
        ORDER BY pertinenza
    )
    SELECT ts.pertinenza ,
    ts.pertinenza / (SELECT MAX(pertinenza) FROM ts ) AS pertinenza_relativa ,
        tbl.*
    FROM ts
    INNER JOIN ski.technics AS tbl
    ON ts.id = tbl.id_technic;
    """
    query_stands = f"""
    WITH ts AS (
        SELECT id,
            ski.ts_normalizer(name_rank,description_rank,notes_rank) AS pertinenza
        FROM ski.get_ts_stands($ts${search}$ts$)
        ORDER BY pertinenza
    )
    SELECT ts.pertinenza ,
    ts.pertinenza / (SELECT MAX(pertinenza) FROM ts ) AS pertinenza_relativa ,
        tbl.*
    FROM ts
    INNER JOIN ski.stands AS tbl
    ON ts.id = tbl.id_stand;
    """

    query_strikingparts = f"""
    WITH ts AS (
        SELECT id,
            ski.ts_normalizer(name_rank,description_rank,notes_rank) AS pertinenza
        FROM ski.get_ts_strikingparts($ts${search}$ts$)
        ORDER BY pertinenza
    )
    SELECT ts.pertinenza ,
    ts.pertinenza / (SELECT MAX(pertinenza) FROM ts ) AS pertinenza_relativa ,
        tbl.*
    FROM ts
    INNER JOIN ski.strikingparts AS tbl
    ON ts.id = tbl.id_part;
    """
    conn = psycopg2.connect(uri)
    cur = conn.cursor()
    cur.execute(query_targets)
    results_targets = cur.fetchall()
    cur.close()
    
    cur = conn.cursor()
    cur.execute(query_technics)
    results_technics = cur.fetchall()
    cur.close()
    
    cur = conn.cursor()
    cur.execute(query_stands)
    results_stands = cur.fetchall()
    cur.close()
    
    cur = conn.cursor()
    cur.execute(query_strikingparts)
    results_strikingparts = cur.fetchall()
    cur.close()
                
    conn.close()

    return {"ts": search , 
            "Targets":results_targets , 
            "Technics":results_technics , 
            "Stands":results_stands , 
            "Striking_parts":results_strikingparts
    }



@app.get("/technic_inventory")
def info_technic_inventory():
    conn = psycopg2.connect(uri)
    cur = conn.cursor()
    cur.execute(f"SELECT id_technic, waza, name, description, notes, resource_url FROM ski.technics;")
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
    conn = psycopg2.connect(uri)
    cur = conn.cursor()
    cur.execute(f"SELECT id_stand, name, description, illustration_url, notes FROM ski.stands;")
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
    conn = psycopg2.connect(uri)
    cur = conn.cursor()
    cur.execute(f"SELECT id_part, name, translation, description, notes, resource_url FROM ski.strikingparts;")
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
    conn = psycopg2.connect(uri)
    cur = conn.cursor()
    cur.execute(f"SELECT id_target, name, original_name, description, notes, resource_url FROM ski.targets;")
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

