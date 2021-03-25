import os


base = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.join(base, 'app.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS =  True
    SECRET_KEY = 'somerandom numbers'
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'src/static/images/')
    ALLOWED_IMAGES =  ['.jpeg', '.png', '.jpg']

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    pass


