from flask import Flask, url_for, render_template, request, Response, redirect
from models import Person, Picture
from werkzeug.utils import secure_filename
from functools import cmp_to_key
from routes.utils import *

def register_upload(app, db):
    @app.route('/upload', methods=['GET', 'POST'])
    def upload():
        if request.method == 'GET':
            images = Picture.query.all()
            imgs = []
            limit = limit_date("")
            for image in images:
                if compare_dates(image.date, limit) > 0: imgs.append(image)

            return render_template('upload.html', imgs=sort_images(imgs))
        elif request.method == 'POST':
            file = request.files['file']
            date = request.form.get('date')

            if date == "":
                date = latest_date()
                date = next_date(date)

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