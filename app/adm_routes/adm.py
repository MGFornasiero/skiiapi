
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