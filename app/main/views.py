
import os	
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from flask_login import login_required,current_user
from ..models import User,Post,Like,Comment,Images
from .forms import UpdateProfile,UploadForm,PostPic
from .. import db, photos




from . import main
from werkzeug.utils import secure_filename
from app import create_app

app=create_app('development')


@main.route('/')
def index():
    return render_template('index.html')

# write post
@main.route('/post/',methods=['GET','POST'])
@login_required
def post():
   posts = Post.query.all()
   form =PostPic()
   if form.validate_on_submit():
      caption= form.caption.data
      feed_picture=form.feed_picture.data
      
      post = Post(caption=caption,feed_picture=feed_picture)
      db.session.add(post)
      db.session.commit()
   
      return redirect(url_for('main.home'))

   return render_template('posts.html',user=current_user,form =form,posts=posts)


# comments route
@main.route('/comment/<post_id>',methods=['POST'])
@login_required
def comment(post_id):
   text = request.form.get('text')

   post = Post.query.filter_by(id=post_id)
   if post:
      comment = Comment(text = text, author=current_user.id, post_id= post_id)
      db.session.add(comment)
      db.session.commit()
   return redirect(url_for('main.home'))

# likes route
@main.route('/like/<post_id>',methods=['GET'])
@login_required
def like(post_id):
   post = Post.query.filter_by(id=post_id).first()
   like =Like.query.filter_by(author=current_user.id, post_id = post_id).first()
   
   if not post:
      flash('Post does not exist',category='error')
   elif like:
      db.session.delete(like)
      db.session.commit()
   else:
      like = Like(author=current_user.id, post_id=post_id)
      db.session.add(like)
      db.session.commit()

   return redirect(url_for('main.home'))


@main.route("/uploadimage",methods=["POST","GET"])
@login_required
def uploadimage():
    user=current_user
    frm=UploadForm()
    if frm.validate_on_submit():
        file=request.files["file"]
        file.save(os.path.join(app.config["UPLOAD_FOLDER"],secure_filename(file.filename)))
       
        
        upload=Images(name=secure_filename(file.filename),uploader_id=user.id)
        db.session.add(upload)
        db.session.commit()
        return redirect(url_for("main.viewimage"))
    return render_template("postpic.html", upload_form=frm,user=user.username)
 
@main.route("/viewimage",methods=["POST","GET"])
@login_required
def viewimage():
    userimages=Images.query.filter_by(uploader_id=current_user.id).all()
    return render_template("imageview.html",name=current_user.username,images=userimages)


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

