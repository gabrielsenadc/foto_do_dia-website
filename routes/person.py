from flask import Flask, url_for, render_template, request, Response, redirect
from models import Person, Picture
from werkzeug.utils import secure_filename
from functools import cmp_to_key
from routes.utils import *

def register_person(app, db):
    @app.route('/person/<name>')
    def person(name):
        name = name.lower()
        people = Person.query.all()

        list = []
        for person in people:
            if person.name == name: list.append(person.date)

        list.sort(reverse=True, key=cmp_to_key(compare_dates))

        return render_template('person.html', name=name.title(), dates=list)