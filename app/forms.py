from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, FieldList, FormField
from wtforms.validators import DataRequired, Length


class NumCourseForm(FlaskForm):
    num_courses = SelectField('Number of Courses', choices=[(1, '1'),
                                                            (2, '2'),
                                                            (3, '3'),
                                                            (4, '4'),
                                                            (5, '5'),
                                                            (6, '6'),
                                                            (7, '7')],
                              validators=[DataRequired()])
    submit = SubmitField('Next')


class AddCourseForm(FlaskForm):
    code = StringField('Course Code*', validators=[Length(min=6, max=9),
                                                   DataRequired()])
    lec_link = StringField('Lecture Link*')
    lec_passcode = StringField('Lecture Passcode (Optional)')
    tut_link = StringField('Tutorial Link (Optional)')
    tut_passcode = StringField('Tutorial Passcode (Optional)')
    pra_link = StringField('Practical Link (Optional)')
    pra_passcode = StringField('Practical Passcode (Optional)')
    lec_code = StringField('Lecture Section Code', validators=[Length(min=3, max=6)])
    tut_code = StringField('Tutorial Section Code (Optional)')
    pra_code = StringField('Practical Section Code (Optional)')

    submit = SubmitField('Next')


class AddClassForm(FlaskForm):
    times = [('', ''), (1, '1'), (2, '2'),
             (3, '3'),
             (4, '4'),
             (5, '5'),
             (6, '6'),
             (7, '7'),
             (8, '8'),
             (9, '9'),
             (10, '10'),
             (11, '11'),
             (12, '12')]
    weekdays = [('', ''), (1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'),
                (4, 'Thursday'), (5, 'Friday')]

    code = StringField('Course Code*', validators=[Length(min=6, max=9),
                                                DataRequired()])

    lec_link = StringField('Lecture Link*')
    tut_link = StringField('Tutorial Link (Optional)')
    pra_link = StringField('Practical Link (Optional)')

    lec1_day= SelectField('Weekday*', choices=weekdays, default=1)
    lec1_start = SelectField('Start Time*', choices=times, default=1)
    lec1_ampm = SelectField('AM/PM*', choices=[('', ''), ('am', 'AM'), ('pm', 'PM')], default='pm')

    lec2_day= SelectField('Weekday', choices=weekdays, default=0)
    lec2_start = SelectField('Start Time', choices=times, default=0)
    lec2_ampm = SelectField('AM/PM', choices=[('', ''), ('am', 'AM'), ('pm', 'PM')])

    lec3_day = SelectField('Weekday', choices=weekdays, default=0)
    lec3_start = SelectField('Start Time', choices=times, default=0)
    lec3_ampm = SelectField('AM/PM', choices=[('', ''), ('am', 'AM'), ('pm', 'PM')])

    tut_day = SelectField('Weekday', choices=weekdays, default=0)
    tut_start = SelectField('Start Time', choices=times, default=0)
    tut_ampm = SelectField('AM/PM', choices=[('', ''), ('am', 'AM'), ('pm', 'PM')])

    pra_day = SelectField('Weekday', choices=weekdays, default=0)
    pra_start = SelectField('Start Time', choices=times, default=0)
    pra_ampm = SelectField('AM/PM', choices=[('', ''), ('am', 'AM'), ('pm', 'PM')])
    submit = SubmitField('Submit')




class TimeForm(FlaskForm):
    times = [(1, '1'), (2, '2'),
             (3, '3'),
             (4, '4'),
             (5, '5'),
             (6, '6'),
             (7, '7'),
             (8, '8'),
             (9, '9'),
             (10, '10'),
             (11, '11'),
             (12, '12')]
    weekdays = [(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'),
                (4, 'Thursday'), (5, 'Friday')]
    start = SelectField('Start Time', choices=times, validators=[DataRequired()])
    start_ampm = SelectField('AM/PM', choices=[('am', 'AM'), ('pm', 'PM')], validators=[DataRequired()])
