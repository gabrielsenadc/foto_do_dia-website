from flask import Flask, url_for, render_template, request, Response
from models import Person, Picture
from werkzeug.utils import secure_filename
from functools import cmp_to_key

class Pessoa():

    def __init__(self, name, first):
        self.name = name
        self.qtd = 1
        self.last = first

    def inc_qtd(self, date):
        self.qtd += 1
        self.last = date

    def get_name(self):
        return self.name

    def __repr__(self):
        return f'{self.name} - {self.qtd}'


def compare_dates(date1, date2):
    day1 = int(date1.split("/")[0])
    month1 = int(date1.split("/")[1])
    year1 = int(date1.split("/")[2])

    day2 = int(date2.split("/")[0])
    month2 = int(date2.split("/")[1])
    year2 = int(date2.split("/")[2])

    if(year1 - year2): return year1 - year2
    if(month1 - month2): return month1 - month2
    return day1 - day2
 
def compare(person1, person2):
    if(person1.qtd - person2.qtd): return person1.qtd - person2.qtd
    return compare_dates(person1.last, person2.last)

def sort_people(people):
    pessoas = []
    for person in people:
        new = 1
        for pessoa in pessoas:
            if pessoa.get_name() == person.name: 
                pessoa.inc_qtd(person.date)
                new = 0
                break
        if new: pessoas.append(Pessoa(person.name, person.date))
    pessoas.sort(reverse=True, key=cmp_to_key(compare))
    return pessoas

def render_index(people):
    pessoas = sort_people(people)

    rank = []
    count = 0
    for pessoa in pessoas:
        if(count >= 5): break
        count += 1
        rank.append(pessoa)

    dates = []
    images = Picture.query.all()
    for image in images:
        dates.append(image.date)

    dates.sort(reverse=True, key=cmp_to_key(compare_dates))

    return render_template('index.html', people=rank, dates=dates)

def register_routes(app, db):

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'GET':
            people = Person.query.all()
            return render_index(people)
        elif request.method == 'POST':
            name = request.form.get('name')
            date = request.form.get('date')

            people = Person.query.all()

            for person in people:
                if person.name == name and person.date == date:
                    return render_index(people)

            person = Person(name=name, date=date)

            db.session.add(person)
            db.session.commit()

            new_people = Person.query.all()
            return render_index(new_people)
    
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
            return render_template('redirect.html')
        
    @app.route('/filter/<day>/<month>/<year>', methods=['GET', 'POST'])
    def filter(day, month, year):
        if request.method == 'GET':
            people = Person.query.all()
            filtered = []

            date = f"{day}/{month}/{year}"

            print(date)
            
            for person in people:
                if person.date == date: filtered.append(person)

            return render_template('sobre.html', people=filtered, date=date)
        if request.method == 'POST':
            name = request.form.get('name')
            date = f"{day}/{month}/{year}"

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

            return render_template('sobre.html', people=filtered, date=date)

         
    @app.route('/upload', methods=['GET', 'POST'])
    def upload():
        if request.method == 'GET':
            imgs = Picture.query.all()
            return render_template('upload.html', imgs=imgs)
        elif request.method == 'POST':
            file = request.files['file']
            date = request.form.get('date')

            if not file:
                return 'No file uploaded!', 400

            filename = secure_filename(file.filename)
            mimetype = file.mimetype
            if not filename or not mimetype:
                return 'Bad upload!', 400

            img = Picture(img=file.read(), name=filename, mimetype=mimetype, date=date)
            db.session.add(img)
            db.session.commit()

            return render_template('redirect.html', date=date)


    @app.route('/<day>/<month>/<year>')
    def get_img(day, month, year):
        date = f"{day}/{month}/{year}"
        img = Picture.query.filter_by(date=date).first()
        if not img:
            return 'Img Not Found!', 404

        return Response(img.img, mimetype=img.mimetype)
    
    @app.route('/delete/<int:id>', methods=['POST'])
    def delete_img(id):
            imgs = Picture.query.all()

            for img in imgs:
                if img.id == id: db.session.delete(img)
            
            db.session.commit()

            imgs = Picture.query.all()
            return render_template('upload.html', imgs=imgs)
    
    @app.route('/ranking')
    def rank():
        people = Person.query.all()
        pessoas = sort_people(people)

        return render_template('rank.html', people=pessoas)