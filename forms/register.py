from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, TextAreaField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    nickname = StringField('Nickname', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Again password', validators=[DataRequired()])
    about = TextAreaField('Description')
    submit = SubmitField('Register')
