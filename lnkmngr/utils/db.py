import sqlite3
import pandas as pd
import numpy as np
from utils.consts import get_lnkmngr_db_path
from utils.consts import CATEGORY_TYPE
from utils import under_str_frmt
import json


db_conn = sqlite3.connect(get_lnkmngr_db_path(), check_same_thread=False)
cursor = db_conn.cursor()


def add_new_table(table_name):
    table_name = table_name.strip()
    assert len(table_name.split(" ")) == 1
    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id        INTEGER PRIMARY KEY,
            parent_id INTEGER,
            type      STRING  NOT NULL,
            label     STRING  NOT NULL,
            href      STRING
        )
        """
    )


def get_all_link_tables():
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    return [(x[0], under_str_frmt(x[0])) for x in cursor.fetchall()]


def read_table(table_name):
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", db_conn)
    df = df.replace({"": None})
    df = df.replace({np.nan: None})
    df = df.set_index(["id"])
    return df


def __get_orph_ids(table_name):
    df = read_table(table_name)
    orph_ids = []
    for id, row in df.iterrows():
        parent_id = row.parent_id
        if parent_id is None:
            continue
        if parent_id not in df.index:
            orph_ids.append(id)
    return orph_ids


def del_entry(table_name, id):
    cursor.execute(
        f"""
        DELETE FROM {table_name}
        WHERE id={id}
        """
    )
    db_conn.commit()

    orph_ids = __get_orph_ids(table_name)
    while orph_ids:
        for orph_id in orph_ids:
            cursor.execute(
                f"""
                DELETE FROM {table_name}
                WHERE id={orph_id}
                """
            )
            db_conn.commit()
        orph_ids = __get_orph_ids(table_name)


def get_table_categories(table_name):
    df = pd.read_sql_query(
        f"SELECT * FROM {table_name} WHERE type='{CATEGORY_TYPE}' ", db_conn
    )
    df = df.replace({"": None})
    df = df.replace({np.nan: None})
    df = df.set_index(["id"])

    res = {}
    for id, row in df.iterrows():
        node = (id, row.label)
        if node not in res:
            res[node] = []

        if row.parent_id is not None:
            pnode = (row.parent_id, df.loc[row.parent_id].label)
            if pnode not in res:
                res[pnode] = []
            else:
                res[pnode].append(node)

    all_cats = []
    cat_map = {}
    for k, v in res.items():
        all_cats.append({"text": k[1], "value": k[0]})
        cat_map[k[0]] = []
        for x in v:
            cat_map[k[0]].append({"text": x[1], "value": x[0]})

    return json.dumps(all_cats), json.dumps(cat_map)


def add_new_entry(table_name, label, type, parent_id, href):
    cursor.execute(
        f"""
        INSERT INTO {table_name} (label, type, parent_id, href)
        VALUES(?, ?, ?, ?)
        """,
        (label, type, parent_id, href),
    )
    db_conn.commit()
    return cursor.lastrowid
