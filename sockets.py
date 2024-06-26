from flask_socketio import SocketIO, join_room, leave_room, emit
from flask import session
from database.db import Db

from models.tictactoe.model import TicTacToe
from models.tictactoe.converters import convert_to_game, convert_to_game_content

MAX_USERS = 2
socketio = SocketIO()

@socketio.on('connect')
def on_join():
    room_id = session.get('room_id')
    if room_id:
        with Db() as db:
            db.add_user_to_room(room_id)
            room = db.get_room(room_id)
        join_room(room_id)
        current_users = room['current_users']
        game_content = room['game_content']
        emit('content-to-client', game_content)
        if current_users >= MAX_USERS:
            with Db() as db:
                db.close_room(room_id)
            emit('start-game-client', to=room_id)

@socketio.on('disconnect')
def on_leave():
    room_id = session.get('room_id')
    if room_id:
        leave_room(room_id)
        with Db() as db:
            db.remove_user_from_room(room_id)
            emit('pause-game-client', to=room_id)

@socketio.on('content-to-server')
def update_game(data):
    room_id = session.get('room_id')
    if room_id:
        with Db() as db:
            game_content = db.get_game_content(room_id)
            game_type = db.get_game_type(room_id)
        game = convert_to_game(game_content)
        col = data['col']
        row = data['row']
        if game_type == 'tictactoe':
            move_success = game.make_move(col, row)
        print(col)
        print(row)
        print(move_success)
        if move_success:
            updated_game_content = convert_to_game_content(game)
            with Db() as db:
                db.update_game_content(room_id, updated_game_content)
            emit('content-to-client', updated_game_content, to=room_id)

@socketio.on('rematch-to-server')
def handle_rematch():
    has_rematched = session.get('has_rematched')
    if not has_rematched:
        room_id = session.get('room_id')
        if room_id:
            with Db() as db:
                db.add_rematch_request(room_id)
                session['has_rematched'] = True
                rematch_requests = db.get_rematch_requests(room_id)
            if rematch_requests >= MAX_USERS:
                with Db() as db:
                    game_type = db.get_game_type(room_id)
                    game_content =  db.get_game_content(room_id)
                    db.reset_rematch_requests(room_id)
                if game_type == 'tictactoe':
                    game = convert_to_game(game_content)
                    game.new_game()
                    updated_game_content = convert_to_game_content(game)
                with Db() as db:
                    db.update_game_content(room_id, updated_game_content)
                emit('content-to-client', updated_game_content, to=room_id)
                emit('rematch-reset-client', to=room_id)

@socketio.on('rematch-reset-server')
def handle_rematch_reset():
    session['has_rematched'] = False
