from typing import Union
import os
from fastapi import FastAPI


        
#import sqlalchemy
#from sqlalchemy import URL
#from sqlalchemy import create_engine
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import sessionmaker
#from sqlalchemy.dialects import postgresql
#from sqlalchemy import select
#from sqlalchemy.sql import text

app = FastAPI()

import psycopg2
uri = "postgresql://postgres:Gion.1982@10.35.144.3:5432/postgres"

@app.get("/")
def read_root():
    return {"Hello": "Karate!!!"}


@app.get("/kihon_list/{grade_id}")
def read_grade(grade_id: int , sequenza: int = 1):
    """
    da grado e tipo restituisce l'elenco delle chiavi dei kihon per tale grado
    """
    query = f"""
    SELECT 
        --inv.number,
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
    cur.close()
    conn.close()
    res = {row[0]:[row[1],row[2],row[3],row[4]] for row in result}
    return {"grade_id": grade_id, "sequenza n":sequenza,"tecniche":res}

@app.get("/grade_inventory")
def grade_inventory():
    conn = psycopg2.connect(uri)
    cur = conn.cursor()
    cur.execute("SELECT grade,gtype, id_grade FROM ski.grades;")
    result = cur.fetchall()
    cur.close()
    conn.close()
    gradi = {res[2]:f"{res[0]}° {res[1]}" for res in results}
    return {"gradi": str(gradi)}

@app.get("/stand_inventory")
def stand_inventory():
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
    conn = psycopg2.connect(uri)
    cur = conn.cursor()
    cur.execute("SELECT id_technic,waza ,name ,description ,notes ,resource_url FROM ski.technics;")
    results = cur.fetchall()
    cur.close()
    conn.close()
    tecniche = {f"{res[1]} ({res[0]})" : f"{res[2]}" for res in results}
    return {"tecniche": tecniche}