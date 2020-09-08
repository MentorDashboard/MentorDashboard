from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.urls import url_parse
from flask_login import login_user

from src import bcrypt
from src.forms.auth import RegisterForm, LoginForm
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
            return render_template('auth/register.html', form=form), 400

        create_user(name, email, password)

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')

        flash('You have successfully registered. You can now login.')
        return redirect(next_page), 201

    return render_template('auth/register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user_by_email(form.email.data)

        if user is None or not bcrypt.check_password_hash(user.password, form.password.data):
            flash('Invalid email address or password')
            return render_template('auth/login.html', title='Sign In', form=form), 401

        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        flash('You have been logged in')
        return redirect(next_page), 201

    return render_template('auth/login.html', form=form)
