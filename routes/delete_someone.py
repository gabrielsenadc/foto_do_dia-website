from flask import Flask, url_for, render_template, request, Response, redirect
from models import Person, Picture
from werkzeug.utils import secure_filename
from functools import cmp_to_key
from routes.utils import *

def register_delete_someone(app, db):
    @app.route('/delete/<name>/<day>/<month>/<year>', methods=['GET', 'POST'])
    def delete_someone(name, day, month, year):
        if request.method == 'GET':
            people = Person.query.all()
            return render_template('sobre.html', people=people)
        elif request.method == 'POST':
            people = Person.query.all()
            date = f"{day}/{month}/{year}"

            for person in people:
                if person.name == name and person.date == date: db.session.delete(person)
            
            db.session.commit()

            people = Person.query.all()
            return render_sobre(people, date, 'main')