from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo


class AddStudentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    course = StringField('Course', validators=[DataRequired()])
    stage = StringField('Stage', validators=[DataRequired()])
    submit = SubmitField('Add Student')
