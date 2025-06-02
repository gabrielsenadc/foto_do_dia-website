from flask import Response
from models import Picture
from routes.utils import *
from flask_login import current_user

def register_get_img(app, db):
    @app.route('/get_img/<date>')
    def get_img(date):
        date = date.replace("_", "/")
        imgs = Picture.query.filter_by(user_id=current_user.id)
        
        for img in imgs:
            if img.date == date: return Response(img.img, mimetype=img.mimetype)

        return 'Img Not Found!', 404