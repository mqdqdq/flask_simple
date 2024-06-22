from flask import Flask
from views import views_bp

from sockets import socketio
import secrets

app = Flask(__name__)
app.register_blueprint(views_bp)
#socketio.init_app(app)
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)