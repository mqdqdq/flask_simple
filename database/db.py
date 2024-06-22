import sqlite3

class ChatDb():

    def __enter__(self):
        self.conn = sqlite3.connect('database.db')
        self.conn.row_factory = sqlite3.Row
        return self

    def __exit__(self, exc_type, exc_val, exc_trace) -> None:
        self.conn.commit()
        self.conn.close()

    def get_room_data(self, room_id):
        try:
            post = self.conn.execute('SELECT * FROM chatrooms WHERE id = ?', (room_id,)).fetchone()
            return post
        except Exception as error:
            print(f"Database error: {error}")
            return None
    
    def add_user_to_room(self, room_id):
        try:
            self.conn.execute('UPDATE chatrooms SET user_count = (user_count + 1) WHERE id = ?', (room_id, ))
        except Exception as error:
            print(f"Database error: {error}")

    def remove_user_from_room(self, room_id):
        try:
            self.conn.execute('UPDATE chatrooms SET user_count = (user_count - 1) WHERE id = ?', (room_id, ))
        except Exception as error:
            print(f"Database error: {error}")

    def add_chat_room(self):
        try:
            self.conn.execute('INSERT INTO chatrooms (user_count) VALUES (0)')
        except Exception as error:
            print(f"Database error: {error}")