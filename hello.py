from flask import Flask, render_template, request, redirect, url_for
from model import *
app = Flask(__name__)


@app.before_request
def before_request():
    # initialize db connection
    initialize_db()


@app.teardown_request
def teardown_request(exception):
    # close db connection
    db.close()


@app.route('/register/')
def register():
    # Render to register page
    return render_template('login_register.html')


@app.route('/new_user/', methods=['POST'])
def new_user():
    # Main logic of registration
    #if request.form['login'] not in User.select().where(User.login == request.form['login']):
    User.create(
            login=request.form['login'],
            password=request.form['pass']
    )
    return redirect(url_for('home'))


@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
