from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import (
    PasswordField,
    StringField,
    SubmitField,
)
from wtforms.fields.html5 import EmailField
from wtforms.validators import (
    Email,
    EqualTo,
    InputRequired,
    Length,
)

from app import db
from app.models import User, Student

class AddStudentForm(FlaskForm):
    student = QuerySelectField(
        'student Name',
        validators=[InputRequired()],
        get_label='id',
        query_factory=lambda: db.session.query(User).order_by('first_name'))    
    mun_id = StringField(
        'Mun ID', validators=[InputRequired(),
                                  Length(1, 64)])
    first_name = QuerySelectField(
        'student Name',
        validators=[InputRequired()],
        get_label='first_name',
        query_factory=lambda: db.session.query(User).order_by('first_name'))
    
    submit = SubmitField('Add Student')

class RegistrationUserForm(FlaskForm):
    first_name = StringField(
        'First name', validators=[InputRequired(),
                                  Length(1, 64)])
    last_name = StringField(
        'Last name', validators=[InputRequired(),
                                 Length(1, 64)])
    email = EmailField(
        'Email', validators=[InputRequired(),
                             Length(1, 64),
                             Email()])
    password = PasswordField(
        'Password',
        validators=[
            InputRequired(),
            EqualTo('password2', 'Passwords must match')
        ])
    password2 = PasswordField('Confirm password', validators=[InputRequired()])
    mun_id = StringField('Mun ID', validators=[InputRequired(),Length(1, 8)])
    university = StringField('University', validators=[InputRequired(),Length(1, 64)])
    submit = SubmitField('Register')