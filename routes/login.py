from flask import url_for, render_template, request, redirect
from models import User
from routes.utils import *
from flask_login import login_user, logout_user, login_required, current_user

def register_login(app, db):
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template('login.html')
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