from flask import Blueprint, render_template, request, redirect, url_for, session
import secrets
from database.db import ChatDb

views_bp = Blueprint("views", __name__, template_folder = "templates")

@views_bp.route('/')
def index():
    with ChatDb() as db:
        chat_contents = db.get_chat_content('JJb407rp')
        messages = [chat_content[2] for chat_content in chat_contents]
        print(messages)
    return render_template('index.html', messages=messages)