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

from app.professor.forms import (
    AddProfessorForm,
    RegistrationUserForm
)

from app.email import send_email
from app.models import User, Professor

professor = Blueprint('professor', __name__, )

@professor.route('/')
def index():
    """Admin dashboard page."""
    return render_template('professor/index.html')


@professor.route('/new', methods=['GET', 'POST'])
def new_professor():
    """Add new professor."""
    form = AddProfessorForm()
    if form.validate_on_submit():
        professor = Professor(
            user = form.professor.data,
            #mun_id = form.mun_id.data,
            
        )
        db.session.add(professor)
        db.session.commit()
        flash('Professor {} successfully created'.format(professor),
              'form-success')
    
    return render_template('professor/new.html', form=form)


@professor.route('/signup', methods=['GET', 'POST'])
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
        professor = Professor(
            user_id=user.id,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            university=form.university.data
        )
        db.session.add(professor)
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
    return render_template('professor/signup.html', form=form)

@professor.route('/professors')
def professors():
    """View all professors."""
    professors = Professor.query.all()
    users = User.query.all()
    return render_template(
        'professor/professors.html', professors=professors, users=users)

@professor.route('/professor/<int:professor_id>')
@professor.route('/professor/<int:professor_id>/info')
def professor_info(professor_id):
    """View a user's profile."""
    professor = Professor.query.filter_by(id=professor_id).first()
    user = Professor.query.filter_by(id=professor_id).first()
    if professor is None:
        abort(404)
    return render_template('professor/professor.html', professor=professor, user=user) 