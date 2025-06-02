from flask import url_for, request, redirect
from models import Person
from routes.utils import *
from flask_login import current_user, login_required

def register_filter(app, db):
    @app.route('/filter/<date>/<source_name>', methods=['GET', 'POST'])
    @login_required
    def filter(date, source_name):
        if request.method == 'GET':
            date = date.replace("_", "/")
            return render_sobre(date, source_name)
        if request.method == 'POST':
            name = request.form.get('name')
            name = name.lower()
            date = date.replace("_", "/")

            people = Person.query.filter_by(user_id=current_user.id)

            for person in people:
                if person.name == name and person.date == date:
                    return redirect(url_for('filter', date=date, source_name=source_name))

            person = Person(name=name, date=date, user_id=current_user.id)

            db.session.add(person)
            db.session.commit()
            
            return render_sobre(date, source_name)
