from flask import Flask, url_for, render_template, request, Response, redirect
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

def compare_imgs(img1, img2):
    return compare_dates(img1.date, img2.date)

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

def sort_images(imgs):
    imgs.sort(reverse=True, key=cmp_to_key(compare_imgs))
    return imgs
    

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

    date = f"{day:02d}/{month:02d}/{year:04d}"

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

def limit_date():
    last_date = latest_date()

    day = int(last_date.split("/")[0])
    month = int(last_date.split("/")[1])
    year = int(last_date.split("/")[2])

    month -= 1
    if month < 1:
        month = 12
        year -= 1

    return f"{day:02d}/{month:02d}/{year:04d}"
        
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
    limit = limit_date()
    for image in images:
        if compare_dates(image.date, limit) > 0: dates.append(image.date)

    dates.sort(reverse=True, key=cmp_to_key(compare_dates))

    start = "01_08_2023"
    end = latest_date().replace("/", "_")

    return render_template('index.html', people=rank, dates=dates, start=start, end=end)

def render_sobre(people, date, source):
    filtered = []

    for person in people:
        if person.date == date: filtered.append(person)

    next = next_date(date)
    previous = previous_date(date)

    if compare_dates(next, latest_date()) > 0: next = None

    if source: source = source.title()

    return render_template('sobre.html', people=filtered, date=date, previous=previous, next=next, source=source)
