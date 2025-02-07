from flask import Flask, url_for, render_template, request, Response, redirect
from models import Person, Picture
from werkzeug.utils import secure_filename
from functools import cmp_to_key
from routes.utils import *

def register_index(app, db):
    
    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'GET':
            people = Person.query.all()
            return render_index(people)
        elif request.method == 'POST':
            name = request.form.get('name')  
            name = name.lower()
            return redirect(url_for("person", name=name))