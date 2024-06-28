from db import Db

with Db() as db:
        with open('database/schema.sql') as f:
            db.conn.executescript(f.read())