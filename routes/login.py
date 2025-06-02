from flask import Flask, url_for, render_template, request, Response, redirect, current_app
from models import Person, Picture, User
from werkzeug.utils import secure_filename
from functools import cmp_to_key
from routes.utils import *
from flask_login import login_user, logout_user, login_required, current_user

def register_login(app, db):
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            users = User.query.all()
            print(current_user)
            return render_template('login.html', users=users)
        elif request.method == 'POST':
            name = request.form.get('name')
            password = request.form.get('password')

            users = User.query.all()
            user_found = False
            for user in users:
                if user.name == name and user.password == password: 
                    login_user(user)
                    print("logged")
                    user_found = True

            if not user_found: return 'Erro'

            return redirect(url_for("index"))
        
    @app.route('/logout', methods=['GET', 'POST'])
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("index"))