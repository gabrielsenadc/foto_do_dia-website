from flask import Flask, url_for, render_template, request, Response, redirect
from models import Person, Picture
from werkzeug.utils import secure_filename
from functools import cmp_to_key
from routes.utils import *

def register_rank(app, db):
    @app.route('/ranking/<start>/<end>')
    def rank(start, end):

        start = start.replace("_", "/")
        end = end.replace("_", "/")

        people = Person.query.all()
        filtered = []
        for person in people:
            if compare_dates(person.date, start) >= 0 and compare_dates(person.date, end) <= 0:
                filtered.append(person)
                
        pessoas = sort_people(filtered)

        if start == "01/08/2023" and end == latest_date(): source = 'main'
        else: source = "between-" + start.replace("/", "_") + '-' + end.replace("/", "_")

        return render_template('rank.html', people=pessoas, source=source)