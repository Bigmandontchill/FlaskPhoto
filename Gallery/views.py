from Gallery.models import Photo
from flask import Blueprint,render_template ,flash ,request,jsonify
from flask_login.utils import login_required
from . import db
from .models import Photo,Like,Comment 
from flask_login import  current_user
import json

views=Blueprint('views',__name__)

@views.route('/our_post',methods=['GET','POST'])
@login_required
def our_photo():
   if request.method=='POST':
      comment=request.form.get('comment')
      photo_id=request.form.get('photo_id')
      check_comment(comment,photo_id)
   photos=Photo.query.all()
   return render_template("our_photo.html",user=current_user,photos=photos,Like=Like,Comment=Comment)



@views.route('/your_post')
@login_required
def your_photo():
   photos=Photo.query.all()
   return render_template("photo.html",user=current_user,photos=photos,Like=Like,Comment=Comment)   

          
def check_comment(comment,photo_id):    
     if (len(comment.strip())<1):   
       flash("Please add your comment",category='error')  
     else:
         my_comment=Comment(photo_id=photo_id,user_id=current_user.id,body=comment)
         db.session.add(my_comment)
         db.session.commit()


@views.route('/add_like', methods=['POST'])
@login_required
def add_like():
    data = json.loads(request.data)
    photoId = data['photoId']
    like=Like.query.filter_by(photo_id=photoId,user_id=current_user.id).first()
    if like:
         flash("you can only like a picture once",category='error')
    else:
         like=Like(photo_id=photoId,user_id=current_user.id)
         db.session.add(like)
         db.session.commit()    
    return jsonify(
                    status=200
                )









