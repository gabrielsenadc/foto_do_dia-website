from flask import Flask, url_for, render_template, request, Response, redirect
from models import Person, Picture
from werkzeug.utils import secure_filename
from functools import cmp_to_key
from routes.utils import *

def register_delete(app, db):
    @app.route('/delete/<int:id>', methods=['POST'])
    def delete_img(id):
            imgs = Picture.query.all()

            for img in imgs:
                if img.id == id: db.session.delete(img)
            
            db.session.commit()

            imgs = Picture.query.all()
            return render_template('upload.html', imgs=imgs)