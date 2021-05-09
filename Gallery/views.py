from flask import Blueprint,render_template ,flash ,request,render_template,jsonify, Flask, flash, request, redirect, url_for
from . import app
from werkzeug.utils import secure_filename
import os

views=Blueprint('views',__name__)


def check_file(filename):
     ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
     return '.' in filename and filename.rsplit('.',1)[1].lower() in  ALLOWED_EXTENSIONS

@views.route('/post',methods=['GET','POST'])
def post():
   if request.method=='POST':
     file=request.files['file'] # get the file 
     process_file(file)
   return render_template("upload_file.html")


def process_file(file):
    if file.filename== '':# if user didn'y select anyfile
        flash('Please select a file to upload',category='error')
    elif file and check_file(file.filename):# if the file is good
         filename=secure_filename(file.filename)
         file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
         flash('you added your photo',category='success') 
    else:
          flash("Don't try something funny",category='error')     

@views.route('/your_photo')
def your_photo():
   return render_template("photo.html")


     
       



