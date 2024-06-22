from flask_socketio import SocketIO, emit
from flask import session

socketio = SocketIO()

@socketio.on('connect')
def on_join():
    emit('client-connect')

@socketio.on('disconnect')
def on_leave():
    emit('client-disconnect')

@socketio.on('server-new-message')
def message(message):
    emit('client-new-message', message)

    