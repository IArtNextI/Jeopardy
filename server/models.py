from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Question(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    scenario = db.Column(db.String)
    answer = db.Column(db.String)
    price = db.Column(db.Integer)

    theme_id = db.Column(db.Integer, db.ForeignKey('theme.id'))


class Theme(db.Model):
    __tablename__ = 'theme'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    round_id = db.Column(db.Integer, db.ForeignKey('round.id'))

    questions = db.relationship('Question')


class Round(db.Model):
    __tablename__ = 'round'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    pack_id = db.Column(db.Integer, db.ForeignKey('pack.id'))

    themes = db.relationship('Theme')


class Pack(db.Model):
    __tablename__ = 'pack'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    difficulty = db.Column(db.Integer)
    author = db.Column(db.String)

    rounds = db.relationship('Round')
