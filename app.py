from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./teste.db'
    app.secret_key = 'segredo'

    bcrypt = Bcrypt(app)

    login_manager = LoginManager(app)
    login_manager.login_view = "login"

    db.init_app(app)

    from models import User

    @login_manager.user_loader
    def user_loader(id):
        return User.query.filter_by(id=id).first()

    from routes.routes_register import register_routes
    
    register_routes(app, db, bcrypt)
    
    migrate = Migrate(app, db)

    return app