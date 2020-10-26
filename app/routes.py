from app import app, db
from flask import render_template, redirect, url_for, flash, session, request, jsonify
from app.forms import *
from app.auth_forms import *
from app.models import User, Course, Practical, Tutorial, Lecture, PushSubscription
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.webpush_handler import trigger_push_notifications_for_subscriptions
import requests


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    courses = Course.query.filter_by(student=current_user).all()
    crslst = []
    for course in courses:
        crs = [course, Lecture.query.filter_by(course=course).first()]
        tut = Tutorial.query.filter_by(course=course).first()
        if tut != 'null':
            crs.append(tut)
        else:
            crs.append(None)
        pra = Practical.query.filter_by(course=course).first()
        if pra != 'null':
            crs.append(pra)
        else:
            crs.append(None)
        crslst.append(crs)

    return render_template('index.html', courses=crslst)


@app.route('/delete_course/<course_code>')
def delete_course(course_code):
    course = Course.query.filter_by(student=current_user, code=course_code).first()
    Course.query.filter_by(student=current_user, code=course_code).delete()
    if course:
        Lecture.query.filter_by(course=course).delete()
        Tutorial.query.filter_by(course=course).delete()
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/info')
def info():
    return render_template('info.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        session.permanent = True
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/add_course', methods=['GET', 'POST'])
@login_required
def add_course():
    form = AddCourseForm()
    if form.validate_on_submit():
        course = Course(code=form.code.data, student=current_user)

        lec = Lecture(course=course, lec_link=form.lec_link.data, lec_pass=form.lec_passcode.data)
        pra = Practical(course=course, pra_link=form.pra_link.data, pra_pass=form.pra_passcode.data)
        tut = Tutorial(course=course, tut_link=form.tut_link.data, tut_pass=form.tut_passcode.data)

        lec.sec = 'Lec ' + form.lec_code.data
        tut.sec = 'Tut ' + form.tut_code.data
        pra.sec = 'Pra' + form.pra_code.data

        params = {'code': form.code.data, 'term': '2020 Fall'}

        course_data = requests.get('https://nikel.ml/api/courses', params=params).json()

        lec_sec = None
        tut_sec = None
        pra_sec = None
        if course_data['response']:
            times = course_data['response'][0]['meeting_sections']
            for sec in times:
                if lec.sec == sec['code']:
                    lec_sec = sec
                if tut.sec == sec['code']:
                    tut_sec = sec
                if pra.sec == sec['code']:
                    pra_sec = sec

        if lec_sec:
            for time in lec_sec['times']:
                if time['day'] == 'monday':
                    lec.time1 = time['start'] / 3600
                if time['day'] == 'tuesday':
                    lec.time2 = time['start'] / 3600
                if time['day'] == 'wednesday':
                    lec.time3 = time['start'] / 3600
                if time['day'] == 'thursday':
                    lec.time4 = time['start'] / 3600
                if time['day'] == 'friday':
                    lec.time5 = time['start'] / 3600

        if tut_sec:
            tut.day1 = tut_sec['times'][0]['day']
            tut.time1 = tut_sec['times'][0]['start'] / 3600
            if len(tut_sec['times']) > 1:
                tut.day2 = tut_sec['times'][1]['day']
                tut.time2 = tut_sec['times'][1]['start'] / 3600

        if pra_sec:
            pra.day1 = pra_sec['times'][0]['day']
            pra.time1 = pra_sec['times'][0]['start'] / 3600


        db.session.add(course)
        if lec_sec:
            db.session.add(lec)
        if tut_sec:
            db.session.add(tut)
        if pra_sec:
            db.session.add(pra)

        db.session.commit()

        return redirect(url_for('index'))

    return render_template('edit2.html', form=form)


@app.route('/add_class', methods=['GET', 'POST'])
@login_required
def add_class():
    form = AddClassForm()
    if form.validate_on_submit():
        course = Course(code=form.code.data, student=current_user,
                        lec_link=form.lec_link.data,
                        pra_link=form.pra_link.data,
                        tut_link=form.tut_link.data)
        lec = Lecture(course=course)
        pra = Practical(course=course)
        tut = Tutorial(course=course)

        if form.lec1_start.data != '':
            add = 12
            if form.lec1_ampm == 'am':
                add = 0
            lec.day1 = int(form.lec1_day.data)
            lec.time1 = int(form.lec1_start.data) + add

        if form.lec2_start.data != '':
            add = 12
            if form.lec2_ampm == 'am':
                add = 0
            lec.day2 = int(form.lec2_day.data)
            lec.time2 = int(form.lec2_start.data) + add

        if form.lec3_start.data != '':
            add = 12
            if form.lec3_ampm == 'am':
                add = 0
            lec.day3 = int(form.lec3_day.data)
            lec.time3 = int(form.lec3_start.data) + add

        if form.tut_start.data != '':
            add = 12
            if form.tut_ampm == 'am':
                add = 0
            tut.day1 = int(form.tut_day.data)
            tut.time1 = int(form.tut_start.data) + add

        if form.pra_start.data != '':
            add = 12
            if form.pra_ampm == 'am':
                add = 0
            pra.day1 = int(form.pra_day.data)
            pra.time1 = int(form.pra_start.data) + add

        db.session.add(course)
        db.session.add(lec)
        db.session.add(tut)
        db.session.add(pra)

        db.session.commit()

        return redirect(url_for('index'))

    return render_template('edit.html', form=form)


@app.route("/api/push-subscriptions", methods=['POST', 'GET'])
def create_push_subscription():
    json_data = request.get_json()
    subscription = PushSubscription.query.filter_by(
        subscription_json=json_data['subscription_json']).first()
    if subscription is None:
        subscription = PushSubscription(
            subscription_json=json_data['subscription_json']
        )
        db.session.add(subscription)
        db.session.commit()
    return jsonify({
        "status": "success"
    })


@app.route("/admin")
def admin_page():
    return render_template("admin.html")


@app.route("/admin-api/trigger-push-notifications", methods=["POST"])
def trigger_push_notifications():
    json_data = request.get_json()
    subscriptions = PushSubscription.query.all()
    results = trigger_push_notifications_for_subscriptions(
        subscriptions,
        json_data.get('title'),
        json_data.get('body')
    )
    return jsonify({
        "status": "success",
        "result": results
    })
