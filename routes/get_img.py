from flask import Flask, url_for, render_template, request, Response, redirect
from models import Person, Picture
from werkzeug.utils import secure_filename
from functools import cmp_to_key
from routes.utils import *

def register_get_img(app, db):
    @app.route('/get_img/<date>')
    def get_img(date):
        date = date.replace("_", "/")
        img = Picture.query.filter_by(date=date).first()
        if not img:
            return 'Img Not Found!', 404

        return Response(img.img, mimetype=img.mimetype)