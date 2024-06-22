from flask_socketio import SocketIO, emit
from flask import session

socketio = SocketIO()

@socketio.on('connect')
def on_join():
    emit('client-connect', broadcast=True)

@socketio.on('disconnect')
def on_leave():
    emit('client-disconnect', broadcast=True)

@socketio.on('server-new-message')
def message(message):
    emit('client-new-message', message, broadcast=True)

    