from flask import Flask, url_for, render_template, request, Response
from models import Person, Picture
from werkzeug.utils import secure_filename

def render_index(people):
    dates = []
    for person in people:
        new = 1
        for date in dates:
            if person.date == date: new = 0
        
        if new == 1: dates.append(person.date)

    dates.sort(reverse=True)

    return render_template('index.html', people=people, dates=dates)

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
        
    @app.route('/delete', methods=['GET', 'POST'])
    def delete():
        if request.method == 'GET':
            people = Person.query.all()
            return render_template('sobre.html', people=people)
    
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