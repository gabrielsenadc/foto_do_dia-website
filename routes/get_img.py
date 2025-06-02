from flask import Flask, url_for, render_template, request, Response, redirect
from models import Person, Picture
from werkzeug.utils import secure_filename
from functools import cmp_to_key
from routes.utils import *
from flask_login import current_user

def register_get_img(app, db):
    @app.route('/get_img/<date>')
    def get_img(date):
        date = date.replace("_", "/")
        imgs = Picture.query.all()
        
        for img in imgs:
            if img.date == date: 
                if img.user_id == current_user.id:
                    return Response(img.img, mimetype=img.mimetype)

        return 'Img Not Found!', 404