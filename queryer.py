import sqlite3
import json


def insert_partition(cursor, partition: list[str], name: str):
    """
    Expects partition to be sorted

    :param cursor:
    :param partition:
    :param name:
    :return:
    """
    for x in range(len(partition)):
        partition[x] = partition[x].capitalize()

    cursor.execute("INSERT OR IGNORE INTO partition(name, partition) "
                   "VALUES ? RETURNING ROWID",
                   (name, json.dumps(sorted(partition))))
    return cursor.fetchone()


def get_partition_by_id(cursor, partition_id: int):
    cursor.execute("SELECT *, ROWID from partition WHERE ROWID = ?", (partition_id,))
    return cursor.fetchone()


def del_partition_by_id(cursor, partition_id: int):
    cursor.execute("DELETE FROM partition WHERE ROWID = ?", (partition_id,))


def ins_object_decided_cache(cursor, obj: str, category: str, partition_id: int, reasoning=""):
    cursor.execute("INSERT INTO object_decided_cache(object, category, reasoning, partition) VALUES (?,?,?,?)",
                   (obj, category, reasoning, partition_id,))


def find_obj_in_cache(cursor, obj: str, partition_id: int):
    cursor.execut("SELECT category FROM object_decided_cache WHERE (object,partition)=(?,?)",
                  (obj, partition_id,))
    return cursor.fetchone()


if __name__ == "__main__":
    con = sqlite3.connect("test.sqlite")
    cur = con.cursor()

    ins_object_decided_cache(cur, "Cats", "Pepper", 2)

    con.commit()
