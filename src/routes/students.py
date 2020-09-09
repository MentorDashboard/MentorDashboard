from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required, current_user

from src.forms.students import AddStudentForm
from src.models.Student import create_student

bp = Blueprint('students', __name__)


@bp.route('/students', methods=['GET'])
def index():
    return render_template('students/index.html')


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
