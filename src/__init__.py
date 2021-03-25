from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_message = "you need to be authenticated in order to access this page".capitalize()
login_manager.login_message_category = "warning"
login_manager.login_view = "src.views.login"

def create_app():
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)
    
    with app.app_context():
        db.create_all()

    from src.views import users

    app.register_blueprint(users, url_prefix='/')
    return app

