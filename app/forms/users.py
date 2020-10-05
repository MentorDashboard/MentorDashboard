from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    PasswordField,
    IntegerField,
)
from wtforms.validators import DataRequired, Email, EqualTo


class UserProfileForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    hourly_rate = IntegerField("Hourly Rate", validators=[DataRequired()])
    submit = SubmitField("Update Profile")


class UserPasswordUpdateForm(FlaskForm):
    password = PasswordField(
        "Password", validators=[DataRequired(), EqualTo("password_confirm")]
    )
    password_confirm = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Change Password")
