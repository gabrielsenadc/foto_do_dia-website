from flask import request, current_app
from routes.utils import *
from flask_login import login_required

def register_index(app, db):
    
    @app.route('/', methods=['GET', 'POST'])
    @login_required
    def index():
        if request.method == 'GET':
            current_app.limit = ""
            return render_index()
        elif request.method == 'POST':
            return render_index(use_anchor=True)