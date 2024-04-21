from tinydb import TinyDB, Query


class DalTinyDB:
    def __init__(self, db_path='db.json'):
        self.db = TinyDB(db_path)

    def insert(self, table_name, data):
        table = self.db.table(table_name)
        table.insert(data)

    def search(self, table_name, key, value):
        table = self.db.table(table_name)
        item_query = Query()
        return table.search(item_query[key] == value)

    def update(self, table_name, data, key, value):
        table = self.db.table(table_name)
        item_query = Query()
        table.update(data, item_query[key] == value)

    def remove(self, table_name, key, value):
        table = self.db.table(table_name)
        item_query = Query()
        table.remove(item_query[key] == value)

    def fetch_all(self, table_name):
        table = self.db.table(table_name)
        return table.all()
