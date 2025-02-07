from flask import Flask, url_for, render_template, request, Response, redirect
from models import Person, Picture
from werkzeug.utils import secure_filename
from functools import cmp_to_key
from routes.utils import *

def register_routes(app, db):

    from routes.index import register_index
    register_index(app, db)
    
    from routes.delete_someone import register_delete_someone
    register_delete_someone(app, db)
        
    from routes.filter import register_filter
    register_filter(app, db)
         
    from routes.upload import register_upload
    register_upload(app, db)

    from routes.get_img import register_get_img
    register_get_img(app, db)

    from routes.delete import register_delete
    register_delete(app, db)
    
    from routes.rank import register_rank
    register_rank(app, db)
    
    from routes.person import register_person
    register_person(app, db)
    
    from routes.between import register_between
    register_between(app, db)
    
        


