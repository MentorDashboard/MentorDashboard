from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required, current_user

from src.forms.students import AddStudentForm
from src.models.Student import create_student, get_mentor_students

bp = Blueprint('students', __name__)


@bp.route('/students', methods=['GET'])
@login_required
def index():
    students = get_mentor_students(current_user.id)
    return render_template('students/index.html', students=students)


@bp.route('/students/new', methods=['POST', 'GET'])
@login_required
def new():
    form = AddStudentForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        course = form.course.data
        stage = form.course.data

        create_student(name, email, course, stage, current_user.id)

        flash('New student saved')

        return redirect(url_for('students.index'))

    return render_template('students/create.html', form=form)
