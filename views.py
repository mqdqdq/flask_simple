from flask import Blueprint, render_template, request, redirect, url_for, session
import secrets
from database.db import ChatDb
from werkzeug.security import generate_password_hash, check_password_hash

views_bp = Blueprint("views", __name__, template_folder = "templates")

@views_bp.route('/join/<string:room_id>', methods=["GET", "POST"])
def join_room(room_id):
    with ChatDb() as db:
        room = db.get_room(room_id)
        chat_contents = db.get_chat_content(room_id)
    if room:
        messages = [chat_content[3] for chat_content in chat_contents] if chat_contents else []
        saved_id = session.get('room_id')
        if saved_id and saved_id == room_id:
            return render_template('room.html', messages=messages)
        elif request.method == 'POST':
            password = request.form['password-field']
            username = request.form['username-field']
            _, password_hash, _ = room
            if check_password_hash(password_hash, password):
                session['room_id'] = room_id
                session['username'] = username
                return render_template('room.html', messages=messages)
        else:
            return render_template('join_room.html')
    return render_template('error.html')


@views_bp.route('/create', methods=["GET", "POST"])
def create_room():
    if request.method == 'POST':
        password_hash = generate_password_hash(request.form['password-field'])
        username = request.form['username-field']
        room_id = secrets.token_urlsafe(6)
        with ChatDb() as db:
            db.add_room(room_id, password_hash)
            session['room_id'] = room_id
            session['username'] = username
            return redirect(url_for('views.join_room', room_id=room_id))
    return render_template('create_room.html')