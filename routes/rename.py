from flask import Flask, url_for, render_template, request, Response, redirect
from models import Person, Picture
from werkzeug.utils import secure_filename
from functools import cmp_to_key
from routes.utils import *

def register_rename(app, db):
    @app.route('/rename', methods=['GET', 'POST'])
    def rename():
        if request.method == 'GET':
            return render_template('rename.html')
        if request.method == 'POST':
            source_name = request.form.get('source_name')
            dest_name = request.form.get('dest_name')
            source_name = source_name.lower()
            dest_name = dest_name.lower()

            people = Person.query.all()

            for person in people:
                if person.name == source_name:
                    db.session.add(Person(name=dest_name, date=person.date))
                    db.session.delete(person)

            db.session.commit()

            return render_template('rename.html')
