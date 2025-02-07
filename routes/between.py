from flask import Flask, url_for, render_template, request, Response, redirect
from models import Person, Picture
from werkzeug.utils import secure_filename
from functools import cmp_to_key
from routes.utils import *

def register_between(app, db):
    @app.route('/between/<date1>/<date2>')
    def between(date1, date2):
        if request.method == 'GET':
            start = date1.replace("_", "/")
            end = date2.replace("_", "/")
            dates = []
            images = Picture.query.all()
            for image in images:
                if compare_dates(image.date, start) >= 0 and compare_dates(image.date, end) <= 0:
                    dates.append(image.date)

            dates.sort(reverse=True, key=cmp_to_key(compare_dates))
            
            people = Person.query.all()
            filtered = []
            for person in people:
                if compare_dates(person.date, start) >= 0 and compare_dates(person.date, end) <= 0:
                    filtered.append(person)
                    
            pessoas = sort_people(filtered)

            rank = []
            count = 0
            for pessoa in pessoas:
                if(count >= 5): break
                count += 1
                rank.append(pessoa)

            return render_template("between.html", dates=dates, start=start, end=end, people=rank)
        
    @app.route('/between_dates', methods=['POST'])
    def between_dates():
        date1 = request.form.get('date1')
        if(date1 == ''): date1 = "01/08/2023"
        date1 = date1.replace("/", "_")

        date2 = request.form.get('date2')
        if(date2 == ''): date2 = latest_date()
        date2 = date2.replace("/", "_")
        return redirect(url_for("between", date1=date1, date2=date2))