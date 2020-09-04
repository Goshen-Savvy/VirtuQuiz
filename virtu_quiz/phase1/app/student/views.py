from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from flask_rq import get_queue

from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)

from app import db

from app.student.forms import (
    AddStudentForm,
    RegistrationUserForm
)

from app.email import send_email
from app.models import User, Student

student = Blueprint('student', __name__, )

@student.route('/')
def index():
    """Admin dashboard page."""
    return render_template('student/index.html')


@student.route('/new', methods=['GET', 'POST'])
def new_student():
    """Add new student."""
    form = AddStudentForm()
    if form.validate_on_submit():
        student = Student(
            user = form.student.data,
            mun_id = form.mun_id.data,
            first_name = form.first_name.data,            
        )
        db.session.add(student)
        db.session.commit()
        flash('Student {} successfully created'.format(student.mun_id),
              'form-success')
    
    return render_template('student/new.html', form=form)

@student.route('/signup', methods=['GET', 'POST'])
def register():
    """Register a new user, and send them a confirmation email."""
    form = RegistrationUserForm()
    if form.validate_on_submit():
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=form.password.data)
        db.session.add(user)
        db.session.commit()
        student = Student(
            user_id=user.id,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            university=form.university.data,
            mun_id=form.mun_id.data
        )
        db.session.add(student)
        db.session.commit()
        token = user.generate_confirmation_token()
        confirm_link = url_for('account.confirm', token=token, _external=True)
        get_queue().enqueue(
            send_email,
            recipient=user.email,
            subject='Confirm Your Account',
            template='account/email/confirm',
            user=user,
            confirm_link=confirm_link)
        flash('A confirmation link has been sent to {}.'.format(user.email),
              'warning')
        return redirect(url_for('main.index'))
    return render_template('student/signup.html', form=form)

@student.route('/students')
def students():
    """View all students."""
    students = Student.query.all()
    users= User.query.all()
    return render_template(
        'student/students.html', students=students, users=users)

@student.route('/<int:student_id>')
@student.route('/<int:student_id>/info')
def student_info(student_id):
    """View a user's profile."""
    student = Student.query.filter_by(id=student_id).first()
    if student is None:
        abort(404)
    return render_template('student/student.html', student=student) 
