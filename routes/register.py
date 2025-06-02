from flask import Flask, url_for, render_template, request, Response, redirect, current_app
from models import Person, Picture, User
from werkzeug.utils import secure_filename
from functools import cmp_to_key
from routes.utils import *
from flask_login import login_user

def register_register(app, db):
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'GET':
            users = User.query.all()
            return render_template('register.html', users=users)
        elif request.method == 'POST':
            name = request.form.get('name')
            password = request.form.get('password')

            user = User(name=name, password=password)
            db.session.add(user)
            db.session.commit()

            return redirect(url_for("login"))