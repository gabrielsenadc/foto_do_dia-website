from flask import url_for, render_template, request, redirect
from models import User
from routes.utils import *

def register_register(app, db, bcrypt):
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'GET':
            return render_template('register.html')
        elif request.method == 'POST':
            name = request.form.get('name')
            password = request.form.get('password')

            hashed_pwd = bcrypt.generate_password_hash(password).decode('utf-8')

            user = User(name=name, password=hashed_pwd)
            db.session.add(user)
            db.session.commit()

            return redirect(url_for("login"))