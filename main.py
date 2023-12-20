import os

from flask import Flask, redirect, render_template, url_for, flash
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from data import db_session
from data.users import User

from forms.register import RegisterForm


templatesDir = os.getcwd() + 'templates'
staticDir = os.getcwd() + '/static'
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config["EXPLAIN_TEMPLATE_LOADING"] = True


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/', methods=['GET', 'POST'])
def index():
    db_sess = db_session.create_session()
    try:
        user = db_sess.query(User).filter(User.id == current_user.id)
        print(user)
        return render_template('index.html', user=user, current_user=current_user, title='Главная')
    except Exception:
        return render_template('index.html', current_user=current_user, title='Главная')
    
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        print(form.nickname.data, form.email.data,
              form.password.data, form.about.data, sep='\n')
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter((User.email == form.email.data) | (User.username == form.nickname.data)).first():
            return render_template('register.html', title='Регистрация',
                                   message="Такой пользователь уже есть")
        user = User()
        user.username = form.nickname.data
        user.email = form.email.data
        # form.avatar.data.save(f'static/img/{form.nickname.data}')
        # user.avatar = url_for('static', filename=f'img/{form.nickname.data}')
        user.avatar = '/static/img/user-icon.png'
        user.set_password(form.password.data)
        user.userdescription = form.about.data
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    else:
        print(form.validate_on_submit(), form.nickname.data, form.email.data,
              form.password.data, form.about.data, sep='\n')
    return render_template('register.html', title='Регистрация', form=form)


def main():
    db_session.global_init('db/mega.db')
    app.run()


if __name__ == '__main__':
    main()
