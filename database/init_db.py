from db import ChatDb

with ChatDb() as db:
        with open('database/schema.sql') as f:
            db.conn.executescript(f.read())
            db.add_room()
            db.add_chat_entry('JJb407rp', 'Hello')
            db.add_chat_entry('JJb407rp', 'How are you?')