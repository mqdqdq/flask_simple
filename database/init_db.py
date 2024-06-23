from db import ChatDb

with ChatDb() as db:
        with open('database/schema.sql') as f:
            db.conn.executescript(f.read())