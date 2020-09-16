from flask import Blueprint, flash, redirect, render_template, url_for, abort
from flask_login import login_required, current_user

from src.forms.students import (
    AddStudentForm,
    EditStudentForm,
    AddStudentNoteForm,
    AddStudentSessionForm,
)
from src.models.Student import (
    create_student,
    get_mentor_students,
    update_student,
    get_student_by_id,
    add_student_note,
    update_contact_date,
    add_student_session,
)

bp = Blueprint("students", __name__)


@bp.route("/students", methods=["GET"])
@login_required
def index():
    students = get_mentor_students(current_user.id)
    return render_template("students/index.html", students=students)


@bp.route("/students/new", methods=["POST", "GET"])
@login_required
def new():
    form = AddStudentForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        course = form.course.data
        stage = form.course.data

        create_student(name, email, course, stage, current_user.id)

        flash("New student saved")
        return redirect(url_for("students.index"))

    return render_template("students/create.html", form=form)


@bp.route("/students/<student_id>")
def view(student_id):
    student = get_student_by_id(student_id)
    add_student_note_form = AddStudentNoteForm()

    if current_user.id is not student.mentor_id:
        return abort(404)

    return render_template(
        "students/view.html",
        student=student,
        add_student_note_form=add_student_note_form,
    )


@bp.route("/students/<student_id>/edit", methods=["POST", "GET"])
def edit(student_id):
    form = EditStudentForm()
    student = get_student_by_id(student_id)
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        course = form.course.data
        stage = form.stage.data
        active = form.active.data

        if not update_student(
            student.id, name, email, course, stage, active, current_user.id
        ):
            return redirect(url_for("students.index")), 403

        flash("Student Successfully Updated")
        return redirect(url_for("students.index"))

    return render_template("students/edit.html", form=form, student=student)


@bp.route("/students/<student_id>/notes", methods=["POST"])
def add_note(student_id):
    form = AddStudentNoteForm()
    student = get_student_by_id(student_id)
    if form.validate_on_submit():
        note = form.note.data

        add_student_note(student.id, note)

        if form.update_contact_date.data == "yes":
            update_contact_date(student_id)

        flash("Note successfully saved", "success")
        return redirect(url_for("students.view", student_id=student.id))

    flash(
        "There was a problem adding this note, make sure you actually add a note",
        "error",
    )
    return render_template(
        "students/view.html", student=student, add_student_note_form=form
    )


@bp.route("/students/<student_id>/sessions", methods=["POST", "GET"])
def add_session(student_id):
    form = AddStudentSessionForm()
    student = get_student_by_id(student_id)
    if form.validate_on_submit():
        date = form.date.data
        duration = form.duration.data
        session_type = form.session_type.data
        project = form.project.data
        summary = form.summary.data
        progress = form.progress.data
        concerns = form.concerns.data
        personal_notes = form.personal_notes.data

        add_student_session(
            student_id,
            date,
            duration,
            session_type,
            project,
            summary,
            progress,
            concerns,
            personal_notes,
        )

        flash("Session successfully saved", "success")
        return redirect(url_for("students.view", student_id=student.id))

    return render_template("students/sessions/create.html", student=student, form=form)
