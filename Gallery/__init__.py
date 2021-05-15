from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db=SQLAlchemy()
DB_NAME="database.db"


UPLOAD_FOLDER = 'Gallery/static'
app=Flask(__name__)
def make_app():
  app.config['SECRET_KEY']='1234'
  app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
  app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_NAME}'
  db.init_app(app)
  from .views import views
  from .auth import auth
  from .models import User,Photo
  make_database(app)
  app.register_blueprint(views,url_prefix='/')
  app.register_blueprint(auth,url_prefix='/')
  return app

def make_database(app):
  if not path.exists('Gallery/'+DB_NAME):
     db.create_all(app=app)


