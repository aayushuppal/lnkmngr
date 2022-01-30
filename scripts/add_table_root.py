import sqlite3

db_path = ""

db_conn = sqlite3.connect(db_path, check_same_thread=False)
cursor = db_conn.cursor()


def update_table(t1):
    cursor.execute(
        f"""
        INSERT INTO {t1} (label, type, parent_id, href)
        VALUES(?, ?, ?, ?)
        """,
        (t1, "category", None, None),
    )
    db_conn.commit()
    new_root_id = cursor.lastrowid

    cursor.execute(
        f"""
        UPDATE {t1}
        SET parent_id = {new_root_id}
        WHERE parent_id IS NULL AND id != {new_root_id}
        """
    )
    db_conn.commit()


for t in []:
    update_table(t)
