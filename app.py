from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from form import *
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

Bootstrap(app)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/vlad/PycharmProjects/FlaskProject/database.db'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))


@app.route('/register/', methods=['GET', 'POST'])
def register():
    # Main logic of registration
    form = RegisterForm()

    if form.validate_on_submit():
        # Hashing password for more security
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data,
                        email=form.email.data,
                        password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('login_register.html', form=form)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                # Flag, for hidden/show log_out system
                check = True
                return render_template('index.html', check=check)
            return '<h1>Invlaid password</h1>'
        return '<h1>Invalid username or password</h1>'

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    check = False
    logout_user()
    return render_template('index.html', check=check)


@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
