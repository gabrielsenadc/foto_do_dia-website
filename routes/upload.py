from flask import render_template, request
from models import Picture
from werkzeug.utils import secure_filename
from routes.utils import *
from flask_login import current_user, login_required

def register_upload(app, db):
    @app.route('/upload', methods=['GET', 'POST'])
    @login_required
    def upload():
        if request.method == 'GET':
            images = Picture.query.all()
            imgs = []
            limit = limit_date()
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

            img = Picture(img=file.read(), name=filename, mimetype=mimetype, date=date, user_id=current_user.id)
            
            db.session.add(img)
            db.session.commit()

            return render_template('redirect.html', date=date)