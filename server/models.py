from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Task(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    scenario = db.Column(db.String)
    answer = db.Column(db.String)
    price = db.Column(db.Integer)

    pack_id = db.Column(db.Integer, db.ForeignKey('pack.id'))


class Pack(db.Model):
    __tablename__ = 'pack'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    difficulty = db.Column(db.Integer)
    author = db.Column(db.String)

    tasks = db.relationship('Task')
