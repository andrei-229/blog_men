import os

from flask import Flask, redirect, render_template, request, url_for, flash
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from data import db_session
from data.users import User

from forms.register import RegisterForm
from forms.login import LoginForm
from forms.edit import EditProfile


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


@app.route('/profile')
def profile():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    return render_template('profile.html', title='Профиль', user=user)


@app.route('/edit_profile', methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfile()
    if request.method == 'GET':
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        # form.nickname.data = user.nickname
        form.about.data = user.userdescription
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        # user.nickname = form.nickname.data
        user.userdescription = form.about.data
        filename = f'{user.username}.png'
        form.icon.data.save(f'static/img/{filename}')
        user.avatar = url_for('static', filename=f'img/{filename}')
        db_sess.commit()
        return redirect('/profile')
    return render_template('edit_profile.html', form=form, title='Редактирование профиля', user=user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/', methods=['GET', 'POST'])
def index():
    db_sess = db_session.create_session()
    try:
        user = db_sess.query(User).filter(User.id == current_user.id)
        print(current_user.name)
        return render_template('index.html', user=user, current_user=current_user, title='Главная')
    except Exception:
        return render_template('index.html', current_user=current_user, title='Главная')
    
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User()
        if form.password.data != form.password_again.data:
            return render_template('register.html',
                                   title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter((User.email == form.email.data) | (User.username == form.nickname.data)).first():
            return render_template('register.html', 
                                   title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user.username = form.nickname.data
        user.email = form.email.data
        user.set_password(form.password.data)
        user.avatar = '/static/img/user-icon.png'
        user.userdescription = form.about.data
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


def main():
    db_session.global_init('db/mega.db')
    app.run()


if __name__ == '__main__':
    main()
