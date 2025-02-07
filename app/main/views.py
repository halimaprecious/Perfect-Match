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
    images = Images.query.order_by(Images.posted.desc()).all()   
    
    return render_template("index.html",images=images,user=current_user)



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
 


@main.route('/profile/<uname>')
def userprofile(uname):
   user = Images.query.filter_by(author=uname).first() 
   images = Images.query.filter_by(author = current_user.id).all()
   # userdata = Images.query.filter_by()
   
    
   if user is None:
    
      return render_template('errors/404.html')
   return render_template("profile/profile.html", user=uname, images= images) 

#user profile
@main.route('/user/<username>')
def profile(username):
   user = User.query.filter_by(username=username).first() 
   images = Images.query.filter_by(author = current_user.id).all()
   return render_template("profile/profile.html", user = user, images= images)


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

# comments route
@main.route('/comment/<post_id>',methods=['POST'])
@login_required
def comment(post_id):
   text = request.form.get('text')

   post = Images.query.filter_by(id=post_id)
   if post:
      comment = Comment(text = text, author=current_user.id, post_id= post_id)
      db.session.add(comment)
      db.session.commit() 
      return redirect(url_for("main.index"))

   return redirect(url_for('main.comment',post_id= post_id))

# likes route
@main.route('/like/<post_id>',methods=['GET'])
@login_required
def like(post_id):
   post = Images.query.filter_by(id=post_id).first()
   like =Like.query.filter_by(author=current_user.id, post_id = post_id).first()
   
   if like:
      db.session.delete(like)
      db.session.commit()
   else:
      like = Like(author=current_user.id, post_id=post_id)
      db.session.add(like)
      db.session.commit()
      return redirect(url_for("main.index"))

   return redirect(url_for('main.comment',post_id=post_id))

