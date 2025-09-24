import sqlite3
import json
import os
from controller.representations import *


class Cacher:
    def __init__(self):
        return

    def fetch(self, obj="", partition=None) -> None | tuple[str, str]:
        # First entry of tuple specifies cat, second specifies reasoning

        print("Please replace this method with another")
        return None

    def insert(self, res: CategorizedNoun, partition: Partition):
        print("Please replace this method with another")
        return None


class QueryObject:
    con: sqlite3.Connection
    cursor: sqlite3.Cursor
    db_address: str
    cacher: None | Cacher

    def __init__(self, address="test.sqlite"):
        self.db_address = address
        self.con = sqlite3.connect(address)
        self.cursor = con.cursor()
        self.cacher = None

    def commit(self):
        self.con.commit()

    def createCacher(self) -> Cacher:
        if self.cacher is not None:
            return self.cacher

        cacher = Cacher()

        def fetch(obj="", partition=None) -> None | tuple[str, str]:
            # First entry of tuple specifies cat, second specifies reasoning

            return self.find_obj_in_cache(obj, partition.partition_id)

        def insert(res: CategorizedNoun, partition: Partition):
            return self.ins_obj_in_cache(res.original_object, res.category, partition.partition_id,
                                         reasoning=res.reasoning)

        cacher.fetch = fetch

        cacher.insert = insert

        self.cacher = cacher

        return cacher

    def insert_partition(self, partition: list[str], name: str):
        """
        Expects partition to be sorted alphabetically

        :param cursor:
        :param partition:
        :param name:
        :return:
        """
        for x in range(len(partition)):
            partition[x] = partition[x].capitalize()

        self.cursor.execute("INSERT OR IGNORE INTO partition(name, partition) "
                       "VALUES ? RETURNING ROWID",
                       (name, json.dumps(sorted(partition))))
        return self.cursor.fetchone()

    def get_partition_by_id(self, partition_id: int):
        self.cursor.execute("SELECT *, ROWID from partition WHERE ROWID = ?", (partition_id,))
        return self.cursor.fetchone()

    def del_partition_by_id(self, partition_id: int):
        self.cursor.execute("DELETE FROM partition WHERE ROWID = ?", (partition_id,))

    def ins_obj_in_cache(self, obj: str, category: str, partition_id: int, reasoning=""):
        self.cursor.execute("INSERT OR IGNORE INTO object_decided_cache(object, category, reasoning, partition) VALUES (?,?,?,?)",
                       (obj, category, reasoning, partition_id,))

    def find_obj_in_cache(self, obj: str, partition_id: int):
        self.cursor.execute("SELECT category FROM object_decided_cache WHERE (object,partition)=(?,?)",
                      (obj, partition_id,))
        return self.cursor.fetchone()


if __name__ == "__main__":
    con = sqlite3.connect("../test.sqlite")
    cur = con.cursor()

    con.commit()
