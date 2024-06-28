import sqlite3, secrets
from werkzeug.security import check_password_hash
import ast

class Db():

    def __enter__(self):
        self.conn = sqlite3.connect('database.db')
        self.conn.row_factory = sqlite3.Row
        return self

    def __exit__(self, exc_type, exc_val, exc_trace) -> None:
        self.conn.commit()
        self.conn.close()

    def add_room(self, room_id, password_hash, game_content, game_type):
        try:
            self.conn.execute('INSERT INTO rooms (room_id, password_hash, game_content, game_type) VALUES (?, ?, ?, ?)', (room_id, password_hash, game_content, game_type, ))
        except Exception as error:
            print(f"Database error: {error}")

    def get_room(self, room_id):
        try:
            room = self.conn.execute('SELECT * FROM rooms WHERE room_id = ?', (room_id, )).fetchone()
            return room
        except Exception as error:
            print(f"Database error: {error}")
            return None
        
    def get_all_rooms(self):
        try:
            rooms = self.conn.execute('SELECT * FROM rooms').fetchall()
            return rooms
        except Exception as error:
            print(f"Database error: {error}")
            return None
        
    def get_game_content(self, room_id):
        try:
            game_content = self.conn.execute('SELECT game_content FROM rooms WHERE room_id = ?', (room_id, )).fetchone()[0]
            game_content = ast.literal_eval(game_content)
            return game_content
        except Exception as error:
            print(f"Database error: {error}")
            return None
        
    def get_game_type(self, room_id):
        try:
            game_type = self.conn.execute('SELECT game_type FROM rooms WHERE room_id = ?', (room_id, )).fetchone()[0]
            return game_type
        except Exception as error:
            print(f"Database error: {error}")
            return None
        
    def update_game_content(self, room_id, game_content):
        try:
            self.conn.execute('UPDATE rooms SET game_content = ? WHERE room_id = ?', (game_content, room_id, ))
        except Exception as error:
            print(f"Database error: {error}")
        
    def add_user_to_room(self, room_id):
        try:
            self.conn.execute('UPDATE rooms SET current_users = current_users + 1 WHERE room_id = ?', (room_id, ))
        except Exception as error:
            print(f"Database error: {error}")
        
    def close_room(self, room_id):
        try:
            self.conn.execute('UPDATE rooms SET room_closed = 1 WHERE room_id = ?', (room_id, ))
        except Exception as error:
            print(f"Database error: {error}")
        
    def remove_user_from_room(self, room_id):
        try:
            self.conn.execute('UPDATE rooms SET current_users = current_users - 1 WHERE room_id = ?', (room_id,))
        except Exception as error:
            print(f"Database error: {error}")
        
    def add_rematch_request(self, room_id):
        try:
            self.conn.execute('UPDATE rooms SET rematch_requests = rematch_requests + 1 WHERE room_id = ?', (room_id,))
        except Exception as error:
            print(f"Database error: {error}")

    def reset_rematch_requests(self, room_id):
        try:
            self.conn.execute('UPDATE rooms SET rematch_requests = 0 WHERE room_id = ?', (room_id,))
        except Exception as error:
            print(f"Database error: {error}")

    def get_rematch_requests(self, room_id):
        try:
            rematch_requests = self.conn.execute('SELECT rematch_requests FROM rooms WHERE room_id = ?', (room_id, )).fetchone()[0]
            return rematch_requests
        except Exception as error:
            print(f"Database error: {error}")
            return None