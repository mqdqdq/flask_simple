from flask_socketio import SocketIO, emit
from flask import session
from database.db import ChatDb

socketio = SocketIO()

@socketio.on('connect')
def on_join():
    with ChatDb() as db:
        db.add_user_to_room('JJb407rp')
        id, user_count = db.get_room('JJb407rp')
    emit('client-connect', user_count, broadcast=True)

@socketio.on('disconnect')
def on_leave():
    with ChatDb() as db:
        db.remove_user_from_room('JJb407rp')
        id, user_count = db.get_room('JJb407rp')
    emit('client-disconnect', user_count, broadcast=True)

@socketio.on('server-new-message')
def message(message):
    with ChatDb() as db:
        db.add_chat_entry('JJb407rp', message)
    emit('client-new-message', message, broadcast=True)

    