from datetime import datetime

from flask import Blueprint, render_template
from flask_login import current_user


from ..models.Student import get_mentor_sessions_between_dates


bp = Blueprint("reports", __name__)


@bp.route("/reports/sessions-report", methods=["GET"])
def sessions_report():
    start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0)
    end = datetime.utcnow()

    sessions = get_mentor_sessions_between_dates(current_user.id, start, end)

    return render_template("reports/sessions.html", sessions=sessions)
