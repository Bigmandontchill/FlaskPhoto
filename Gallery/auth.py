from flask import Blueprint,render_template,request,flash ,redirect ,url_for
from flask.globals import session
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User
from flask_login import login_user, login_required, logout_user, current_user
import re
auth=Blueprint('auth',__name__)
photo='views.our_photo'

@auth.route('/sign_in',methods=['GET','POST'])
def sign_in():
   if(current_user.is_authenticated):
      return redirect(url_for(photo))
   if(request.method=='POST' and check_user()):
      return redirect(url_for(photo))
   return render_template("sign_in.html", user=current_user)

def check_user():
   email=request.form.get('email')
   password=request.form.get('password')
   user=User.query.filter_by(email=email).first()
   if user and check_password_hash(user.password,password):
      flash('logged in susccessful',category='success')
      login_user(user,remember=True)
      return True 
   flash('in correct password',category='error')      
   return False      

@auth.route('/',methods=['GET','POST'])
def sign_up():  
    validate=False
    if(current_user.is_authenticated):
      return redirect(url_for(photo))
    if  request.method=='POST': 
       validate=valdation()
    if(validate):
       return redirect(url_for(photo))
    return render_template("sign_up.html",user=current_user)

@auth.route('/sign_out')
@login_required
def sign_out():
   logout_user()
   return redirect(url_for('auth.sign_in'))

def valdation(): 
    email=request.form.get('email')
    first_name=request.form.get('firstname')
    password1=request.form.get('password1')
    password2=request.form.get('password2')
    if not re.match("[^@]+@[^@]+\.[^@]+", email):
       flash("email in wrong format",category='error')
    elif len(first_name)<2:
       flash("name need to have more than one character",category='error')
    elif len(password1)<8:
       flash("password need to have atleast 8 letters",category='error')
    elif not re.search('[A-Z]',password1):
       flash("password needs to have a capital letter",category='error') 
    elif password1!=password2:
       flash("password are not the same",category='error') 
    else: 
       user=User(email=email,first_name=first_name,password=generate_password_hash(password1,method='sha256'))
       db.session.add(user)
       db.session.commit()
       login_user(user,remember=True)
       return True 
    return False


