from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import FileField, PasswordField, StringField, SubmitField, EmailField, TextAreaField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[
                       DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField(
        'Again password', validators=[DataRequired()])
    nickname = StringField('Username', validators=[DataRequired()])
    about = TextAreaField('Description')
    submit = SubmitField('Register')
