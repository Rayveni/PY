from flask import Flask

from .admin import admin_bp
from .main_app import main_app_bp

app = Flask(__name__)
app.secret_key = 'random string'
app.static_folder = 'static'

app.register_blueprint(admin_bp)
app.register_blueprint(main_app_bp)
