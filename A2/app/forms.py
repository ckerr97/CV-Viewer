from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField, RadioField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError('Username not found.')

class EditProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    company = StringField('Company Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    contact_no = IntegerField('Contact Number (+44)', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    body = TextAreaField('Leave a comment', validators=[DataRequired(), Length(min=1, max=500)])
    rating = RadioField('Rating', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')])
    submit = SubmitField('Submit')

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    company = StringField('Company Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    contact_no = IntegerField('Contact Number (+44)', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=40)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password'), Length(min=5, max=40)])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username')
    

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email.')