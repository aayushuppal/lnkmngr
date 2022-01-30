import sqlite3
import pandas as pd
import numpy as np
from utils.consts import get_lnkmngr_db_path
from utils.consts import CATEGORY_TYPE
from utils import under_str_frmt
import json


db_conn = sqlite3.connect(get_lnkmngr_db_path(), check_same_thread=False)
cursor = db_conn.cursor()


def is_valid_table_name(tn):
    assert len(tn.split(" ")) == 1


def add_new_table(table_name):
    table_name = table_name.strip()
    is_valid_table_name(table_name)
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
    add_new_entry(table_name, table_name, "category", None, None)


def drop_table(table_name):
    table_name = table_name.strip()
    is_valid_table_name(table_name)
    cursor.execute(
        f"""
        DROP TABLE IF EXISTS {table_name}
        """
    )


def rename_table(tn, ntn):
    tn = tn.strip()
    ntn = ntn.strip()
    is_valid_table_name(tn)
    is_valid_table_name(ntn)
    cursor.executescript(
        f"""
        PRAGMA foreign_keys = 0;

        CREATE TABLE {ntn} (
            id        INTEGER PRIMARY KEY,
            parent_id INTEGER,
            type      STRING  NOT NULL,
            label     STRING  NOT NULL,
            href      STRING
        );

        INSERT INTO {ntn} (id, parent_id, type, label,href)
        SELECT id, parent_id, type, label, href FROM {tn};

        DROP TABLE {tn};

        PRAGMA foreign_keys = 1;
        """
    )


def get_all_link_tables():
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name ASC")
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


def update_entry_parent(table_name, id, parent_id):
    cursor.execute(
        f"""
        UPDATE {table_name}
        SET parent_id = {"null" if parent_id is None else parent_id}
        WHERE id = {id}
        """
    )
    db_conn.commit()


def update_entry(table_name, id, label, href):
    cursor.execute(
        f"""
        UPDATE {table_name} SET
        label = "{label}",
        href = "{href}"
        WHERE id = {id}
        """
    )
    db_conn.commit()


def merge_tables(t1, t2, ntn):
    cursor.execute(f"SELECT MAX(id) FROM {t1}")
    t1_max_id = cursor.fetchone()[0]

    cursor.execute(f"SELECT MAX(id) FROM {t2}")
    t2_max_id = cursor.fetchone()[0]

    for i in range(t1_max_id, 0, -1):
        cursor.execute(f"UPDATE {t1} SET id = (id + {t2_max_id}) WHERE id = {i}")
    cursor.execute(
        f"UPDATE {t1} SET parent_id = (parent_id + {t2_max_id}) WHERE parent_id IS NOT NULL"
    )
    db_conn.commit()

    rename_table(t1, ntn)

    copy_rows_to_table(t2, ntn)
    drop_table(t2)

    new_root_id = add_new_entry(ntn, ntn, "category", None, None)
    cursor.execute(
        f"""
        UPDATE {ntn}
        SET parent_id = {new_root_id}
        WHERE parent_id IS NULL AND id != {new_root_id}
        """
    )
    db_conn.commit()


def copy_rows_to_table(t1, t2):
    cursor.execute(f"SELECT id, parent_id, type, label, href FROM {t1}")
    t1_rows = cursor.fetchall()
    for r in t1_rows:
        cursor.execute(
            f"""
            INSERT INTO {t2} (id, parent_id, type, label, href)
            VALUES(?, ?, ?, ?, ?)
            """,
            (r[0], r[1], r[2], r[3], r[4]),
        )
    db_conn.commit()
