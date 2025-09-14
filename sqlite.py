import sqlite3
import json


def insert_partition(cursor, partition: list[str], name: str):
    cursor.execute("INSERT OR IGNORE INTO partition(name, partition) "
                   "VALUES ? RETURNING ROWID",
                   (name, json.dumps(partition)))
    return cursor.fetchone()


def get_partition_by_id(cursor, partition_id: int):
    cursor.execute("SELECT *, ROWID from partition WHERE ROWID = ?", (partition_id,))
    return cursor.fetchone()


def del_partition_by_id(cursor, partition_id: int):
    cursor.execute("DELETE FROM partition WHERE ROWID = ?", (partition_id,))


if __name__ == "__main__":
    con = sqlite3.connect("test.sqlite")
    cur = con.cursor()

    cur.execute("INSERT OR IGNORE INTO partition(name, partition) VALUES ('Table Condiments', "
                "'[\"Salt\", \"Pepper\", \"Vinegar\"]')");

    cur.execute("SELECT *, ROWID FROM partition WHERE name='Table Condiments'")
    f = cur.fetchone()

    print(get_partition_by_id(cur, 2))

    print(get_partition_by_id(cur, 1))

    con.commit()
