from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    courses = db.relationship('Course', backref='student', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10))
    lectures = db.relationship('Lecture', backref='course', lazy='dynamic')
    tutorials = db.relationship('Tutorial', backref='course', lazy='dynamic')
    practicals = db.relationship('Practical', backref='course', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return self.code.upper()


class Lecture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sec = db.Column(db.String(10))
    time1 = db.Column(db.Integer, index=True)
    time2 = db.Column(db.Integer, index=True)
    time3 = db.Column(db.Integer, index=True)
    time4 = db.Column(db.Integer, index=True)
    time5 = db.Column(db.Integer, index=True)
    lec_link = db.Column(db.String(50))
    lec_pass = db.Column(db.String(10))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))

    def __repr__(self):
        return self.sec.upper()


class Tutorial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sec = db.Column(db.String(10))
    day1 = db.Column(db.Integer)
    day2 = db.Column(db.Integer)
    time1 = db.Column(db.Integer)
    time2 = db.Column(db.Integer)
    tut_link = db.Column(db.String(50))
    tut_pass = db.Column(db.String(10))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))

    def __repr__(self):
        return self.sec.upper()

    def day(self, num: int) -> str:
        days = ['Null', 'Mon', 'Tues', 'Wed', 'Thurs', 'Fri']
        return days[self.eval('day' + num)]


class Practical(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sec = db.Column(db.String(10))
    day1 = db.Column(db.Integer, index=True)
    time1 = db.Column(db.Integer, index=True)
    pra_link = db.Column(db.String(50))
    pra_pass = db.Column(db.String(10))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))

    def __repr__(self):
        return self.sec.upper()

    def day(self):
        days = ['Null', 'Mon', 'Tues', 'Wed', 'Thurs', 'Fri']
        return days[self.day1]


class PushSubscription(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    subscription_json = db.Column(db.Text, nullable=False)
