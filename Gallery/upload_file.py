from flask import Blueprint,render_template ,flash ,request
from flask_login.utils import  login_required
from . import app,db
from .models import Photo
from werkzeug.utils import secure_filename
from flask_login import  current_user
import os 

upload_file=Blueprint('upload_file',__name__)

def check_file(filename):
     """ check if the file is the correct type or not
    Args:
        filename ([str]): name of the file 
    Returns:
        [Boolean]: true-> if file has the correct extension
    """
     ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
     return '.' in filename and filename.rsplit('.',1)[1].lower() in  ALLOWED_EXTENSIONS

@upload_file.route('/post',methods=['GET','POST'])
@login_required
def post(): 
   """
   Display the post picture page , and prcess the user's picture"""
   if request.method=='POST':
     file=request.files['file'] # get the file 
     process_file(file)
   return render_template("upload_file.html",user=current_user)


def process_file(file):
    """ check if the user selects the picture or not.
        Add the path of the picture to the database if the user sumbits it correctly
    Args:
        file ([File]): the picture that the user wants to post 
    """
    description=request.form.get('description')
    if (len(description.strip())<1):   
       flash("Please add your description",category='error')   
    elif file.filename== '':# if user didn'y select anyfile
        flash('Please select a file to upload',category='error')
    elif file and check_file(file.filename):# if the file is good
         filename=secure_filename(file.filename)
         file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
         photo = Photo(description=description, path='static/'+filename,user_id=current_user.id)
         db.session.add(photo)
         db.session.commit()
         flash('you added your photo',category='success') 
    else:
          flash("Wrong file type. ALLOWED_EXTENSIONS are'png', 'jpg', 'jpeg'",category='error')  