from datetime import datetime
from math import floor
from decimal import Decimal

from flask import Blueprint, render_template
from flask_login import current_user, login_required

from app.models.Student import (
    get_mentor_sessions_between_dates,
    get_mentor_active_students_by_contact,
)

bp = Blueprint("reports", __name__)


@bp.route("/reports/sessions-report", methods=["GET"])
@login_required
def sessions_report():
    start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0)
    end = datetime.utcnow()

    sessions = get_mentor_sessions_between_dates(current_user.id, start, end)
    duration_mins = calculate_sessions_duration_min_mins(sessions)
    duration = format_duration_string(duration_mins)
    invoice_amount = Decimal(
        (duration_mins / 60) * (current_user.hourly_rate / 100)
    ).quantize(Decimal(10) ** -2)

    return render_template(
        "reports/sessions.html",
        sessions=sessions,
        duration=duration,
        invoice_amount=invoice_amount,
    )


@bp.route("/reports/student-activity-report", methods=["GET"])
@login_required
def student_activity_report():
    students = get_mentor_active_students_by_contact(current_user.id)

    return render_template("reports/activity_report.html", students=students)


def calculate_sessions_duration_min_mins(sessions):
    duration_mins = 0
    for session in sessions:
        duration_mins += session.duration

    return duration_mins


def format_duration_string(duration_mins):
    hours = floor(duration_mins / 60)
    mins = duration_mins % 60
    mins = mins if len(str(mins)) > 1 else f"0{mins}"

    return f"{hours} Hours and {mins} minutes"
