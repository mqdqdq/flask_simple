from flask import Blueprint, render_template, request, redirect, url_for, session
import secrets

views_bp = Blueprint("views", __name__, template_folder = "templates")

@views_bp.route('/')
def index():
    return render_template('index.html')