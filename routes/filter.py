from flask import Flask, url_for, render_template, request, Response, redirect
from models import Person, Picture
from werkzeug.utils import secure_filename
from functools import cmp_to_key
from routes.utils import *
from flask_login import current_user, login_required

def register_filter(app, db):
    @app.route('/filter/<date>/<source_name>', methods=['GET', 'POST'])
    @login_required
    def filter(date, source_name):
        if request.method == 'GET':
            date = date.replace("_", "/")
            return render_sobre(date, source_name)
        if request.method == 'POST':
            name = request.form.get('name')
            name = name.lower()
            date = date.replace("_", "/")

            people = Person.query.all()

            for person in people:
                if person.name == name and person.date == date and person.user_id == current_user.id:
                    return redirect(url_for('filter', date=date, source_name=source_name))

            person = Person(name=name, date=date, user_id=current_user.id)

            db.session.add(person)
            db.session.commit()
            
            return render_sobre(date, source_name)
