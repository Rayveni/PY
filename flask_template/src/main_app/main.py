from flask import render_template
from . import main_app_bp

@main_app_bp.route("/")
def index():
    data = {}
    data['trees'] = ['oak', 'fir', 'ash']
    data['sections'] = ['leaves', 'roots', 'rings']
    data['years'] = list(range(1975, 1980))

    return render_template('index.html')
