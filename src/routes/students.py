from math import floor

import htmlentities
from flask import Blueprint, flash, redirect, render_template, url_for, abort, session
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
    create_student_session,
    update_student_session,
    get_session_by_id,
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
@login_required
def view(student_id):
    student = get_student_by_id(student_id)
    add_student_note_form = AddStudentNoteForm()

    if not student:
        return abort(404)

    if current_user.id is not student.mentor_id:
        return abort(404)

    return render_template(
        "students/view.html",
        student=student,
        add_student_note_form=add_student_note_form,
    )


@bp.route("/students/<student_id>/edit", methods=["POST", "GET"])
@login_required
def edit(student_id):
    form = EditStudentForm()
    student = get_student_by_id(student_id)
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        course = form.course.data
        stage = form.stage.data
        active = True if form.active.data == "yes" else False

        if not update_student(
            student.id, name, email, course, stage, active, current_user.id
        ):
            return redirect(url_for("students.index")), 403

        flash("Student Successfully Updated")
        return redirect(url_for("students.index"))

    return render_template("students/edit.html", form=form, student=student)


@bp.route("/students/<student_id>/notes", methods=["POST"])
@login_required
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
@login_required
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

        student_session = create_student_session(
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

        if form.send_feedback.data == "yes":
            session["feedback_url"] = generate_feedback_url(
                student, student_session, current_user
            )

        flash("Session successfully saved", "success")
        return redirect(url_for("students.view", student_id=student.id))

    return render_template("students/sessions/create.html", student=student, form=form)


@bp.route("/students/<student_id>/sessions/<session_id>/edit", methods=["GET", "POST"])
@login_required
def update_session(student_id, session_id):
    form = AddStudentSessionForm()
    student = get_student_by_id(student_id)
    session = get_session_by_id(session_id)
    if form.validate_on_submit():
        date = form.date.data
        duration = form.duration.data
        session_type = form.session_type.data
        project = form.project.data
        summary = form.summary.data
        progress = form.progress.data
        concerns = form.concerns.data
        personal_notes = form.personal_notes.data

        update_student_session(
            student_id,
            session_id,
            date,
            duration,
            session_type,
            project,
            summary,
            progress,
            concerns,
            personal_notes,
        )

        flash("Session successfully updated", "success")
        return redirect(url_for("students.view", student_id=student_id))

    return render_template(
        "students/sessions/edit.html", student=student, form=form, session=session
    )


def generate_feedback_url(student, student_session, mentor):
    """
    Generates URL to autofill CI session feedback
    :param student:
    :param student_session:
    :param mentor:
    :return: string
    """
    types = {
        "other": "Other",
        "intro": "Intro",
        "inception": "Project inception",
        "middle": "Middle of project",
        "end": "End of project",
        "prep": "Interview preparation and career advice",
        "no-show": "**No-show**",
    }

    projects = {
        "other": "Other",
        "UCFD": "User Centric Front End Development",
        "IFD": "Interactive Front End Development",
        "DCD": "Data Centric Development",
        "FSFwD": "Full Stack Frameworks with Django",
    }

    progress = {
        "poor": "I'm worried about this student's progress.",
        "average": "Average - The student is moving at an acceptable pace.",
        "excellent": "Excellent - It's going great.",
    }

    hours = floor(student_session.duration / 60)
    mins = str(student_session.duration % 60)
    mins = mins if len(mins) > 1 else f"0{mins}"
    duration = f"0{hours}:{mins}:00"

    feedbackurl = "https://docs.google.com/forms/d/e/1FAIpQLSfUCSyObKZDjjtAhIgc8r5FrA4VSUflq1dMK6QyYMv33LeEDQ/viewform?c=0&w=1"
    feedbackurl += f"&emailAddress={htmlentities.encode(mentor.email)}"
    feedbackurl += f"&entry.1191000917={htmlentities.encode(student_session.date.strftime('%Y-%m-%d'))}"
    feedbackurl += f"&entry.1269347964={htmlentities.encode(student.email)}"
    feedbackurl += (
        f"&entry.1521715512={htmlentities.encode(types[student_session.session_type])}"
    )
    feedbackurl += (
        f"&entry.478142644={htmlentities.encode(projects[student_session.project])}"
    )
    feedbackurl += f"&entry.775489883={htmlentities.encode(duration)}"
    feedbackurl += (
        f"&entry.2010663110={htmlentities.encode(progress[student_session.progress])}"
    )
    feedbackurl += f"&entry.1882714143={htmlentities.encode(student_session.summary)}"
    feedbackurl += f"&entry.401267824={htmlentities.encode(student_session.concerns)}"
    feedbackurl += "&emailReceipt=true"

    return feedbackurl
