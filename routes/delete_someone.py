from flask import render_template, request
from models import Person
from routes.utils import *

def register_delete_someone(app, db):
    @app.route('/delete/<name>/<day>/<month>/<year>', methods=['POST'])
    def delete_someone(name, day, month, year):
        people = Person.query.filter_by(user_id=current_user.id)
        date = f"{day}/{month}/{year}"

        for person in people:
            if person.name == name and person.date == date: db.session.delete(person)
        
        db.session.commit()

        return render_sobre(date, 'main')