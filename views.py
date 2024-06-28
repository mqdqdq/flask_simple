from flask import Blueprint, render_template, request, redirect, url_for, session
from database.db import Db
import secrets
from werkzeug.security import generate_password_hash, check_password_hash

from models.tictactoe.model import TicTacToe
from models.tictactoe.converters import convert_to_game_content

views_bp = Blueprint("views", __name__, template_folder = "templates")

@views_bp.route('/', methods=["GET", "POST"])
@views_bp.route('/create', methods=["GET", "POST"])
def create_room():
    if request.method == 'POST':
        game_type = request.form['gametype']
        password = request.form['password']
        room_id = secrets.token_urlsafe(6)
        if game_type == 'tictactoe':
            game_content = convert_to_game_content(TicTacToe())
        with Db() as db:
            db.add_room(room_id, generate_password_hash(password), game_content, game_type)
        session['room_id'] = room_id
        session['player'] = 1
        return redirect(url_for('views.join_room', room_id=room_id))
    else:
        return render_template('create_room.html')

@views_bp.route('/join/<string:room_id>', methods=["GET", "POST"])
def join_room(room_id):
    with Db() as db:
        room = db.get_room(room_id)
    if room:
        saved_room_id = session.get('room_id')
        game_type = room['game_type']
        room_closed = room['room_closed']
        password_hash = room['password_hash']
        if saved_room_id == room_id:
            if game_type == 'tictactoe':
                return render_template('tictactoe.html')
        if request.method == 'POST':
            password = request.form['password']
            if not bool(room_closed) and check_password_hash(password_hash, password):
                session['room_id'] = room_id
                session['player'] = 2
                return redirect(url_for('views.join_room', room_id=room_id))
        else:
            return render_template('join_room.html')
    else:
        return render_template('error.html')