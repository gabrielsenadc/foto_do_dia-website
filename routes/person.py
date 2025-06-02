from flask import url_for, render_template, request, redirect
from models import Person
from functools import cmp_to_key
from routes.utils import *

def register_person(app, db):
    @app.route('/person/<name>')
    def person(name):
        name = name.lower()
        people = Person.query.filter_by(user_id=current_user.id)

        list = []
        for person in people:
            if person.name == name: list.append(person.date)

        list.sort(reverse=True, key=cmp_to_key(compare_dates))

        return render_template('person.html', name=name.title(), dates=list)
    
    @app.route('/person', methods=['POST'])
    def redirect_person():
        name = request.form.get('name')  
        name = name.lower()
        return redirect(url_for("person", name=name))