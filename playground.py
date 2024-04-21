from dal_tinydb import DalTinyDB
import os
import sys
sys.path.append(os.path.dirname(__file__))
db = DalTinyDB()

table = db.fetch_all('approved_domains')
print(os.path.join(
            os.path.dirname(__file__), 'db.json'))
