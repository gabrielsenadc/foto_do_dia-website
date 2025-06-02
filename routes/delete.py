from flask import redirect, url_for
from models import Picture
from routes.utils import *

def register_delete(app, db):
    @app.route('/delete/<int:id>', methods=['POST'])
    def delete_img(id):
            imgs = Picture.query.all()

            for img in imgs:
                if img.id == id: db.session.delete(img)
            
            db.session.commit()

            return redirect(url_for('upload'))