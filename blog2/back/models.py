from datetime import datetime

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(255),nullable=False)
    is_delete = db.Column(db.Boolean, default=0)
    tel = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(20), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    # art = db.Column(db.Integer,db.ForeignKey('art.id'))

    __tablename__ = 'user'

    def save(self):
        db.session.add(self)
        db.session.commit()


class ArticleType(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    t_name = db.Column(db.String(10), unique=True, nullable=False)
    arts = db.relationship('Article', backref='tp')

    __tablename__ = 'art_type'


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(30), unique=True, nullable=False)
    desc = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    good_num = db.Column(db.Integer, default=0)
    count = db.Column(db.Integer, default=0)
    type = db.Column(db.Integer, db.ForeignKey('art_type.id'))
    a_c = db.relationship('Comment', backref='ca')
    # a_u = db.relationship('User', backref='ua')

    __tablename__ = 'art'


c_u = db.Table('c_u',
               db.Column('cid',db.Integer,db.ForeignKey('comment.id'),primary_key=True),
               db.Column('uid',db.Integer,db.ForeignKey('user.id'),primary_key=True )
               )


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    article = db.Column(db.Integer, db.ForeignKey('art.id'))
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    time = db.Column(db.DateTime, default=datetime.now)
    coms = db.relationship('User', secondary=c_u, backref='coms')

    __tablename__ = 'comment'

