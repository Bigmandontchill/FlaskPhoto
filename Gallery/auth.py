from flask import Blueprint,render_template ,flash ,request,render_template,jsonify, Flask, flash, request, redirect, url_for
import re
auths=Blueprint('auths',__name__)

@auths.route('/sign_in')
def sign_in():
  return render_template("sign_in.html")

@auths.route('/',methods=['GET','POST'])
def sign_up():  
    validate=False  
    if request.method=='POST': 
       validate=valdation()
    if(validate):
       return redirect(url_for('views.your_photo'))
    return render_template("sign_up.html")

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
       return True 
    return False


