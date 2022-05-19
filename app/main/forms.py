
from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,TextAreaField, SubmitField,ValidationError,IntegerField,SelectField
from wtforms.validators import DataRequired,Email
from flask_login import current_user
from ..models import User

class PostPic(FlaskForm):
    feed_picture = FileField('feed picture', validators=[FileAllowed(['jpg','png'])])
    caption = TextAreaField('Blog Content',validators=[DataRequired()])
    submit = SubmitField('Update')



class UpdateProfile(FlaskForm):
    username =StringField("Username",validators=[DataRequired()])
    email = StringField("Email",validators=[DataRequired()])
    gender =SelectField('Gender', choices=[('Male','Male'), ('Female', 'Female')],
                           validators=[DataRequired()])
    occupation = TextAreaField("Occupation",validators=[DataRequired()])
    age = IntegerField("Age",validators=[DataRequired()])
    location = TextAreaField("Location",validators=[DataRequired()])
    race= TextAreaField("Race",validators=[DataRequired()])
    bio = TextAreaField("Bio",validators=[DataRequired()])
    
    submit = SubmitField("Update",validators=[DataRequired()]) 

    
class UploadForm(FlaskForm):
    file=FileField('Add a File',validators=[DataRequired()])
    submit=SubmitField('Upload')

