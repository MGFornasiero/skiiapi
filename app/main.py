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
def kihon(grade_id: int , sequenza: int):
    """
    da compilare
    """
    query = f"""
    SELECT 
        seq.seq_num,
        tx.movement ,
        CASE
             WHEN seq.gyaku THEN CONCAT('(Gyaku) ',ski.get_technic_name(seq.techinc))
             ELSE  ski.get_technic_name(seq.techinc)
        END AS tecnica,
        ski.get_stand_name(seq.stand) AS posizione ,
        seq.target_hgt
    FROM ski.kihon_sequences AS seq
    INNER JOIN ski.kihon_inventory AS inv
    ON seq.inventory_id = inv.id_inventory
    LEFT JOIN ski.kihon_tx AS tx 
    ON seq.id_sequence = tx.to_seq 
    WHERE inv.grade_id = {grade_id}
    AND inv.number = {sequenza}
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
    res = {row[0]:{"movement":row[1],"tecnica":row[2],"Stand":row[3],"Target":row[4]} for row in result}
    grade = f"{grade_data[0]}° {grade_data[1]}"
    return {"grade": grade, "grade_id": grade_id, "sequenza_n":sequenza,"tecniche":res}

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
             WHEN seq.gyaku THEN CONCAT('(Gyaku) ',ski.get_technic_name(seq.techinc))
             ELSE  ski.get_technic_name(seq.techinc)
        END AS tecnica,
        ski.get_stand_name(seq.stand) AS posizione ,
        seq.target_hgt
    FROM ski.kihon_sequences AS seq
    INNER JOIN ski.kihon_inventory AS inv
    ON seq.inventory_id = inv.id_inventory
    LEFT JOIN ski.kihon_tx AS tx 
    ON seq.id_sequence = tx.to_seq 
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
    res = [{"sequenza" :row[0] , "ordine":row[1],"movement":row[2],"tecnica":row[3],"Stand":row[4],"Target":row[5]} for row in result]
    
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
    cur.close()
    conn.close()
    print(steps_result)
    print(tx_result)
    res_steps = {step[2]:{'id_sequence' : step[0] , 'kata_id' : step[1] , 'seq_num' : step[2] , 'stand_id' : step[3] , 'posizione' : step[4] , 'guardia' : step[5] , 'facing' : step[6] , 'tecniche' : step[7] , 'embusen' : step[8] , 'kiai' : step[9]} for step in  steps_result}
    res_tx = [{"id_tx":tx[0] , "from_seq":tx[1] , "to_seq":tx[2] , "tempo":tx[3]  , "direction":tx[4]} for tx in tx_result]
    return {"kata_id": kata_id, "steps":res_steps , "transactions":res_tx}




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

@app.get("/stand_inventory")
def stand_inventory():
    """
    segnaposto per l'endpoint ma da metter bene
    """
    conn = psycopg2.connect(uri)
    cur = conn.cursor()
    cur.execute("SELECT id_stand ,name ,description ,illustration_url ,notes FROM ski.stands;")
    results = cur.fetchall()
    cur.close()
    conn.close()
    posizioni = {f"{res[1]} ({res[0]})" : f"{res[2]}" for res in results}
    return {"posizioni": posizioni}

@app.get("/technics_inventory")
def technics_inventory():
    """
    segnaposto per l'endpoint ma da metter bene
    """
    conn = psycopg2.connect(uri)
    cur = conn.cursor()
    cur.execute("SELECT id_technic,waza ,name ,description ,notes ,resource_url FROM ski.technics;")
    results = cur.fetchall()
    cur.close()
    conn.close()
    tecniche = {f"{res[1]} ({res[0]})" : f"{res[2]}" for res in results}
    return {"tecniche": tecniche}

@app.get("/kata_inventory")
def technics_inventory():
    conn = psycopg2.connect(uri)
    cur = conn.cursor()
    cur.execute("SELECT  id_kata , kata ,serie , starting_leg , Note , resource_url FROM ski.Kata_inventory;")
    results = cur.fetchall()
    cur.close()
    conn.close()
    kata = {res[1]:res[0] for res in results}
    return {"kata": kata}

@app.get("/find_technics")
def technics_inventory(query:str = ""):
    """
    segnaposto per l'endpoint ma decidere meglio l'implementazione
    """
    query = f"""
    SELECT tech.id_technic
    , ranking_name
    , ranking_description
    , tech.name
    , tech.description
    FROM (
      SELECT id_technic 
      , ts_rank(ts_name,to_tsquery('tsuki'),16) as ranking_name
      , ts_rank(ts_description,to_tsquery('tsuki'),16) as ranking_description
      FROM ski.ts_technics as findings ) AS ts
    INNER JOIN ski.technics AS tech
    ON ts.id_technic = tech.id_technic 
    WHERE ranking_name >0 OR ranking_description >0
    ORDER BY ts.ranking_name, ts.ranking_description
    ;
    """
    conn = psycopg2.connect(uri)
    cur = conn.cursor()
    cur.execute("SELECT id_technic,waza ,name ,description ,notes ,resource_url FROM ski.technics;")
    results = cur.fetchall()
    cur.close()
    conn.close()
    tecniche = {f"{res[1]} ({res[0]})" : f"{res[2]}" for res in results}
    return {"tecniche": tecniche}