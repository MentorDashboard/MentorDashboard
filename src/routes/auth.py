from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.urls import url_parse

from src.forms.auth import RegisterForm
from src.models.User import create_user, get_user_by_email

bp = Blueprint('auth', __name__)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        if get_user_by_email(email):
            flash('A user already exists with that email address!')
            return redirect(url_for('auth.register')), 400

        create_user(name, email, password)

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')

        flash('You have successfully registered. You can now login.')
        return redirect(next_page), 201

    return render_template('auth/register.html', form=form)


@bp.route('/login', methods=['GET'])
def login():
    return render_template('auth/login.html')
