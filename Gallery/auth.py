from flask import Blueprint,render_template,request,flash ,redirect ,url_for
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User
from flask_login import login_user, login_required, logout_user, current_user
import re
auth=Blueprint('auth',__name__)
photos='views.our_photo'

@auth.route('/sign_in',methods=['GET','POST'])
def sign_in():
   """Display the sign_in page
   Redirect the user to the our_posts page if the user is authenticated or the user sign in sucessfully
   """
   if(current_user.is_authenticated):
      return redirect(url_for(photos))
   if(request.method=='POST' and check_user()):
      return redirect(url_for(photos))
   return render_template("sign_in.html", user=current_user)

def check_user():
   """ check user's email and password
   Returns:
       [Boolean]: return true -> if user enters the correct password and email
                  false -> otherwise
   """
   email=request.form.get('email')
   password=request.form.get('password')
   user=User.query.filter_by(email=email).first()
   if user and check_password_hash(user.password,password):
      flash('logged in susccessful',category='success')
      login_user(user,remember=True)
      return True 
   flash('Incorrect account or password',category='error')      
   return False      

@auth.route('/',methods=['GET','POST'])
def sign_up():  
    """Display the sign_up page
   Redirect the user to the our_posts page if the user is authenticated or the user sign up sucessfully"""
    validate=False
    if(current_user.is_authenticated):
      return redirect(url_for(photos))
    if request.method=='POST': 
        validate=valdation()
    if(validate):
       return redirect(url_for(photos))
    return render_template("sign_up.html",user=current_user)

@auth.route('/sign_out')
@login_required
def sign_out():
   """Log a user out and delete the cookies for the user. redirect the user to sign_in page 
   """
   logout_user()
   return redirect(url_for('auth.sign_in'))

def valdation(): 
    """ Add the user's detail to the database if user enters the correct detail
    Returns:
       [Boolean]:  return true-> if user enters the correct password ,email and name  return false->otherwise 
   """
    email=request.form.get('email')
    first_name=request.form.get('firstname')
    password1=request.form.get('password1')
    password2=request.form.get('password2')
    user=User.query.filter_by(email=email).first()
    if not re.match("[^@]+@[^@]+\.[^@]+", email):
       flash("email in wrong format",category='error')
    elif (user):
       flash("email already exist",category='error')
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


