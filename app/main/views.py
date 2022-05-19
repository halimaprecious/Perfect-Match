
import os	
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from flask_login import login_required,current_user
from ..models import User,Like,Comment,Images
from .forms import UpdateProfile,UploadForm
from .. import db, photos



from . import main
from werkzeug.utils import secure_filename
from app import create_app

app=create_app('development')


@main.route('/')
def index():
    # posts = Images.query.order_by(Images.posted.desc()).all()   
    images = Images.query.order_by(Images.posted.desc()).all()   
    
    # images=Images.query.filter_by(uploader_id=current_user.id).all()
    
    return render_template("index.html",images=images, name= current_user.username)

#user profile on index
@main.route('/user/<username>')
def profindex(username):
   user = User.query.filter_by(username=username).first()

   return render_template("profindex.html", user = user)

@main.route("/uploadimage",methods=["POST","GET"])
@login_required
def uploadimage():
    user=current_user
    frm=UploadForm()
    if frm.validate_on_submit():
        caption = frm.caption.data
        file=request.files["file"]
        file.save(os.path.join(app.config["UPLOAD_FOLDER"],secure_filename(file.filename)))

       
        upload=Images(name=secure_filename(file.filename),author=user.id, caption= caption)
        db.session.add(upload)
        db.session.commit()
        return redirect(url_for("main.index"))
    return render_template("postpic.html", upload_form=frm,user=user.username)
 
# @main.route("/viewimage",methods=["POST","GET"])
# @login_required
# def viewimage():
#     userimages=Images.query.filter_by(uploader_id=current_user.id).all()
#     return render_template("imageview.html",name=current_user.username,images=userimages)


#user profile
@main.route('/user/<username>')
def profile(username):
   user = User.query.filter_by(username=username).first()

   return render_template("profile/profile.html", user = user)

#update profile
@main.route('/user/<username>/update',methods =['GET','POST'])
@login_required
def update_profile(username):
   user = User.query.filter_by(username = username).first()

   form = UpdateProfile()
   if form.validate_on_submit():
        
        username= form.username.data
        user.email = form.email.data
        user.race = form.race.data
        user.age = form.age.data
        user.gender = form.gender.data
        user.location = form.location.data
        user.occupation = form.occupation.data
        user.bio = form.bio.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.profile',username=user.username))

   return render_template('profile/update.html',form =form)


#profile pic
@main.route('/user/<username>/update/pic',methods=['POST'])
@login_required
def update_pic(username):
   user = User.query.filter_by(username=username).first()
   if 'photo' in request.files:
      filename = photos.save(request.files['photo'])
      path = f'photos/{filename}'
      user.profile_pic_path = path
      db.session.commit()

   return redirect(url_for('main.profile',username=username))

