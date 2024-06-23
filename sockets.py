from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import session
from database.db import ChatDb

socketio = SocketIO()

@socketio.on('connect')
def on_join():
    room_id = session.get('room_id')
    if room_id:
        with ChatDb() as db:
            db.add_user_to_room(room_id)
            _, _, user_count = db.get_room(room_id)
        join_room(room_id)
        emit('client-connect', user_count, to=room_id)

@socketio.on('disconnect')
def on_leave():
    room_id = session.get('room_id')
    if room_id:
        with ChatDb() as db:
            db.remove_user_from_room(room_id)
            _, _, user_count = db.get_room(room_id)
        leave_room(room_id)
        emit('client-disconnect', user_count, to=room_id)

@socketio.on('server-new-message')
def message(message):
    room_id = session.get('room_id')
    if room_id:
        with ChatDb() as db:
            db.add_chat_entry(room_id, message)
        emit('client-new-message', message, to=room_id)