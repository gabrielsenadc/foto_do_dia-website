from flask import url_for, render_template, request, redirect
from models import User
from routes.utils import *

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