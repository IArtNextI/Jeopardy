from flask import Flask, render_template
from parser import parsePack
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
db.app = app
db.init_app(app)
db.create_all()

@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/parse')
def parse():
    content = parsePack('./Desyaty_batalion')
    return 'Done!'


@app.route('/new_pack')
def new_pack():
    db.session.add(Pack(name='test_pack', difficulty=5, author='amogus'))
    db.session.commit()
    return 'Done!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
