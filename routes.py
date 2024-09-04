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

def latest_date():
    images = Picture.query.all()

    date = "01/08/2023"

    for image in images:
        if compare_dates(date, image.date) < 0: date = image.date

    return date

def next_date(date):
    day = int(date.split("/")[0])
    month = int(date.split("/")[1])
    year = int(date.split("/")[2])

    day += 1

    if(month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12):
        if(day > 31):
            day = 1
            month += 1     
    elif(month == 2):
        if(year % 4 == 0):
            if(day > 29):
                day = 1
                month += 1      
        else:
            if(day > 28):
                day = 1
                month += 1    
    else:
        if(day > 30):
            day = 1
            month += 1

    if(month > 12):
        month = 1
        year += 1

    latest = latest_date()
    date = f"{day:02d}/{month:02d}/{year:04d}"

    if compare_dates(date, latest) > 0: return None
    return date
    

def previous_date(date):
    day = int(date.split("/")[0])
    month = int(date.split("/")[1])
    year = int(date.split("/")[2])

    day -= 1
    if day == 0:
        month -= 1
        if(month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12):
            day = 31
        elif(month == 2):
            if(year % 4 == 0):
                day = 29      
            else:
                day = 28 
        else:
            day = 30
    if month == 0:
        year -= 1
        month = 12

    date = f"{day:02d}/{month:02d}/{year:04d}"
    if compare_dates(date, "01/08/2023") < 0: return None
    return date
            
        

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

def render_sobre(people, date):
    filtered = []

    for person in people:
        if person.date == date: filtered.append(person)

    next = next_date(date)
    previous = previous_date(date)

    return render_template('sobre.html', people=filtered, date=date, previous=previous, next=next)

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
            date = f"{day}/{month}/{year}"
            
            return render_sobre(people, date)
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

            people = Person.query.all()  
            return render_sobre(people, date)

         
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