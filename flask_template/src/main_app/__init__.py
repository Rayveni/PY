from flask import Blueprint
main_app_bp = Blueprint("main_app_bp", __name__, template_folder='../templates')
from . import main