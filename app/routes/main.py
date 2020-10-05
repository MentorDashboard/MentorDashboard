from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required

from app.models.Student import (
    get_mentor_students,
    get_mentor_active_students,
    get_mentor_sessions_between_dates,
)

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    return render_template("index.html")


@bp.route("/dashboard")
@login_required
def dashboard():
    start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0)
    end = datetime.utcnow()

    total_students = get_mentor_students(current_user.id)
    active_students = get_mentor_active_students(current_user.id)
    month_sessions = get_mentor_sessions_between_dates(current_user.id, start, end)

    return render_template(
        "dashboard.html",
        total_students=total_students,
        active_students=active_students,
        month_sessions=month_sessions,
    )
