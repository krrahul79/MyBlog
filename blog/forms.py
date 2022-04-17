from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, HiddenField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Regexp, Length, Email
from blog.models import User


class RegisterForm(FlaskForm):

    def validate_email(self, email_to_check):
        user = User.query.filter_by(email=email_to_check.data).first()
        if user:
            raise ValidationError(
                'Sorry, there is a problem with your registration')

    #  accessed on 20-01-2022 to find the regex of alphanumeric characters
    #  https://howtodoinjava.com/java/regex/regex-alphanumeric-characters
    first_name = StringField(label='First Name :', validators=[DataRequired(), Regexp(
        '^[A-Za-z0-9]+$', message='Your password contain invalid characters.'), Length(min=2, max=20)])
    email = StringField(label='Email : ', validators=[DataRequired(), Email(
        message='Invalid email. Please check.'), Length(min=2, max=20)])
    password = PasswordField(label='Password : ', validators=[DataRequired(), Regexp(
        '^[A-Za-z0-9]+$', message='Your password contain invalid characters.'), Length(min=6, max=20)])
    repeat_password = PasswordField(label='Confirm Password :', validators=[DataRequired(), Length(
        min=6, max=20), EqualTo('password', message='Passwords do not match. Please try again.')])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):

    email = StringField(label='Email : ', validators=[
                        DataRequired(), Email(), Length(min=2, max=20)])
    password = PasswordField(label='Password : ', validators=[
                             DataRequired(), Length(min=6, max=20)])
    submit = SubmitField(label='Login')


class CommentForm(FlaskForm):
    comment = TextAreaField('Text')
    submit = SubmitField(label='Post')


class DateForm(FlaskForm):
    order = SelectField(
        'Sort By', choices=[('date_asc', 'date_asc'), ('date_desc', 'date_desc')])


class StarForm(FlaskForm):
    postid = HiddenField()
    starrating = HiddenField()
