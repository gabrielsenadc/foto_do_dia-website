from flask import Flask, url_for, render_template, request, Response, redirect, current_app
from models import Person, Picture
from werkzeug.utils import secure_filename
from functools import cmp_to_key
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