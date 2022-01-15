from flask import Flask
from parser import parsePack
from models import *
from pprint import pprint
import json

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
db.app = app
db.init_app(app)
db.create_all()


@app.route('/')
def hello_world():
    return 'Hello, World!'


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
