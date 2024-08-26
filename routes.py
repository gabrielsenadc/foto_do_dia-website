from flask import Flask, url_for, render_template, request
from models import Person

def render_index(people):
    ages = []
    for person in people:
        new = 1
        for age in ages:
            if person.age == age: new = 0
        
        if new == 1: ages.append(person.age)

    ages.sort(reverse=True)

    return render_template('index.html', people=people, ages=ages)

def register_routes(app, db):

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'GET':
            people = Person.query.all()
            return render_index(people)
        elif request.method == 'POST':
            name = request.form.get('name')
            age = request.form.get('age')

            people = Person.query.all()

            for person in people:
                if person.name == name and person.age == int(age):
                    return render_index(people)

            person = Person(name=name, age=age)

            db.session.add(person)
            db.session.commit()

            new_people = Person.query.all()
            return render_index(new_people)
        
    @app.route('/delete', methods=['GET', 'POST'])
    def delete():
        if request.method == 'GET':
            people = Person.query.all()
            return render_template('sobre.html', people=people)
    
    @app.route('/delete/<name>', methods=['GET', 'POST'])
    def delete_someone(name):
        if request.method == 'GET':
            people = Person.query.all()
            return render_template('sobre.html', people=people)
        elif request.method == 'POST':
            people = Person.query.all()

            for person in people:
                if person.name == name: db.session.delete(person)
            
            db.session.commit()

            people = Person.query.all()
            return render_template('redirect.html')
        
    @app.route('/filter/<int:age>', methods=['GET', 'POST'])
    def filter(age):
         if request.method == 'GET':
            people = Person.query.all()
            filtered = []
            
            for person in people:
                if person.age == age: filtered.append(person)

            return render_template('sobre.html', people=filtered)
