from flask import Flask, Response, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user
from flask_login import login_required, current_user
from flask_login import logout_user
from parser import parsePack
from models import *
from pprint import pprint
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
db.app = app
db.init_app(app)
db.create_all()
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler     # In unauthorized_handler we have a callback URL 
def unauthorized_callback():            # In call back url we can specify where we want to 
       return redirect(url_for('login')) 


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login')) # if the user doesn't exist or password is wrong, reload the page
    
    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('profile'))


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    if user:
        flash('Email address already exists')
        return redirect(url_for('signup'))

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('login'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/parse')
def parse():
    content = parsePack('./Desyaty_batalion')
    content = content['package']

    new_pack = Pack(
        name=content['@name'],
        difficulty=content['@difficulty'],
        author=content['info']['authors']['author'],
    )

    for round_ in content['rounds']['round']:
        new_round = Round(name=round_['@name'])
        new_pack.rounds.append(new_round)

        themes = round_['themes']['theme']
        if type(themes) != list:
            themes = [themes]
        for theme in themes:
            new_theme = Theme(name=theme['@name'])
            new_round.themes.append(new_theme)

            questions = theme['questions']['question']
            if type(questions) != list:
                questions = [questions]
            for question in questions:
                price = question['@price']
                answer = question['right']['answer']
                scenario = str(question['scenario']['atom'])
                new_question = Question(
                    price=price,
                    answer=answer,
                    scenario=scenario,
                )
                new_theme.questions.append(new_question)
                db.session.add(new_question)
            db.session.add(new_theme)
        db.session.add(new_round)
    db.session.add(new_pack)
    db.session.commit()

    return 'Done!'


@app.route('/new_pack')
def kek():
    db.session.add(Pack(name='test_pack', difficulty=5, author='amogus'))
    db.session.commit()
    return 'Done!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
