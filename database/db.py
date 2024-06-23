import sqlite3, secrets

class ChatDb():

    def __enter__(self):
        self.conn = sqlite3.connect('database.db')
        self.conn.row_factory = sqlite3.Row
        return self

    def __exit__(self, exc_type, exc_val, exc_trace) -> None:
        self.conn.commit()
        self.conn.close()

    def get_room(self, room_id):
        try:
            room = self.conn.execute('SELECT * FROM rooms WHERE room_id = ?', (room_id,)).fetchone()
            return room
        except Exception as error:
            print(f"Database error: {error}")
            return None
    
    def add_user_to_room(self, room_id):
        try:
            self.conn.execute('UPDATE rooms SET user_count = (user_count + 1) WHERE room_id = ?', (room_id, ))
        except Exception as error:
            print(f"Database error: {error}")

    def remove_user_from_room(self, room_id):
        try:
            self.conn.execute('UPDATE rooms SET user_count = (user_count - 1) WHERE room_id = ?', (room_id, ))
        except Exception as error:
            print(f"Database error: {error}")

    def add_room(self):
        try:
            #room_id = secrets.token_urlsafe(6)
            room_id = 'JJb407rp'
            self.conn.execute('INSERT INTO rooms (room_id) VALUES (?)', (room_id, ))
        except Exception as error:
            print(f"Database error: {error}")

    def get_chat_content(self, room_id):
        try:
            chat_content = self.conn.execute('SELECT * FROM chats WHERE room_id = ?', (room_id, )).fetchall()
            return chat_content
        except Exception as error:
            print(f"Database error: {error}")
            return None
        
    def add_chat_entry(self, room_id, chat_text):
        try:
            self.conn.execute('INSERT INTO chats (room_id, chat_text) VALUES (?, ?)', (room_id, chat_text, ))
        except Exception as error:
            print(f"Database error: {error}")