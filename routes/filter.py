from flask import Flask, url_for, render_template, request, Response, redirect
from models import Person, Picture
from werkzeug.utils import secure_filename
from functools import cmp_to_key
from routes.utils import *

def register_filter(app, db):
    @app.route('/filter/<date>/<source_name>', methods=['GET', 'POST'])
    def filter(date, source_name):
        if request.method == 'GET':
            people = Person.query.all()
            date = date.replace("_", "/")
            
            return render_sobre(people, date, source_name)
        if request.method == 'POST':
            name = request.form.get('name')
            name = name.lower()
            date = date.replace("_", "/")

            people = Person.query.all()

            for person in people:
                if person.name == name and person.date == date:
                    return render_index(people)

            person = Person(name=name, date=date)

            db.session.add(person)
            db.session.commit()

            new_people = Person.query.all()
            filtered = []

            for person in new_people:
                if person.date == date: filtered.append(person)

            people = Person.query.all()  
            
            return render_sobre(people, date, source_name)
