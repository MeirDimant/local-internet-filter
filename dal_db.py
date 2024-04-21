import json
from pathlib import Path
from core.singleton_pattern import Singleton


class DalDB(metaclass=Singleton):
    def __init__(self, db_path='db.json'):
        self.db_path = Path(db_path)
        self.db_path.touch(exist_ok=True)
        self.load_db()

    def load_db(self):
        with self.db_path.open() as f:
            self.db = json.load(f) if self.db_path.stat().st_size != 0 else {}

    def save_db(self):
        with self.db_path.open('w') as f:
            json.dump(self.db, f, indent=4)

    def insert(self, table_name, data):
        if table_name not in self.db:
            self.db[table_name] = []
        self.db[table_name].append(data)
        self.save_db()

    def search(self, table_name, key, value):
        return [item for item in self.db.get(table_name, []) if item.get(key) == value]

    def update(self, table_name, data, key, value):
        table = self.db.get(table_name, [])
        for item in table:
            if item.get(key) == value:
                item.update(data)
        self.save_db()

    def remove(self, table_name, key, value):
        self.db[table_name] = [item for item in self.db.get(
            table_name, []) if item.get(key) != value]
        self.save_db()

    def fetch_all(self, table_name):
        return self.db.get(table_name, [])
