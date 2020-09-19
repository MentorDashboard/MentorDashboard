from flask import Blueprint, render_template, redirect, url_for, abort, flash, session
from flask_login import login_required

from ..models.User import (
    get_user_by_id,
    change_user_password,
    update_user,
    get_all_users,
)
from ..forms.users import UserPasswordUpdateForm, UserProfileForm

bp = Blueprint("users", __name__)


@bp.route("/users", methods=["GET"])
@login_required
def list():
    if not session["is_admin"]:
        return abort(404)

    users = get_all_users()

    return render_template("users/list.html", users=users)


@bp.route("/users/<user_id>", methods=["GET"])
@login_required
def show(user_id):
    user = get_user_by_id(user_id)
    password_form = UserPasswordUpdateForm()
    profile_form = UserProfileForm()

    if not user:
        return abort(404)

    return render_template(
        "users/show.html",
        user=user,
        password_form=password_form,
        profile_form=profile_form,
    )


@bp.route("/users/<user_id>/password", methods=["POST"])
@login_required
def change_password(user_id):
    form = UserPasswordUpdateForm()
    if form.validate_on_submit():
        change_user_password(user_id, form.password.data)

        flash("Password successfully updated", "success")
        return redirect(url_for("users.show", user_id=user_id))


@bp.route("/users/<user_id>/profile", methods=["POST"])
@login_required
def update_profile(user_id):
    form = UserProfileForm()
    if form.validate_on_submit():
        update_user(user_id, form.name.data, form.email.data, form.hourly_rate.data)

        flash("Profile data successfully updated", "success")
        return redirect(url_for("users.show", user_id=user_id))
