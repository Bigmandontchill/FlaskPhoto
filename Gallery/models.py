from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func 

class User(db.Model,UserMixin):
   id=db.Column(db.Integer, primary_key=True)
   email=db.Column(db.String(150), unique=True)
   password=db.Column(db.String(150))
   first_name=db.Column(db.String(150))  
   photos=db.relationship('Photo',backref='user', lazy=True) 
   comments=db.relationship('Comment',backref='user',lazy=True)

   
class Photo(db.Model):
   id=db.Column(db.Integer,primary_key=True)    
   description=db.Column(db.String(10000))
   path=db.Column(db.String(150))
   date=db.Column(db.DateTime(timezone=True),default=func.now())
   user_id=db.Column(db.Integer,db.ForeignKey('user.id'))# a user can have many pictures 

class Like(db.Model):
  # a user can only like a picture once
  photo_id=db.Column(db.Integer,db.ForeignKey('photo.id'),primary_key=True)
  user_id=db.Column(db.Integer,db.ForeignKey('user.id'), primary_key=True)

class Comment(db.Model):
    # a user can have many comments
  id=db.Column(db.Integer, primary_key=True)
  photo_id=db.Column(db.Integer,db.ForeignKey('photo.id'))
  user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
  body=db.Column(db.String(10000))




