from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email


class AddStudentForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    course = StringField("Course", validators=[DataRequired()])
    stage = StringField("Stage", validators=[DataRequired()])
    submit = SubmitField("Add Student")


class EditStudentForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    course = StringField("Course", validators=[DataRequired()])
    stage = StringField("Stage", validators=[DataRequired()])
    active = BooleanField("Active")
    submit = SubmitField("Update Student")


class AddStudentNoteForm(FlaskForm):
    note = TextAreaField("Note", validators=[DataRequired()])
    update_contact_date = SelectField(
        "Update Contact Date", validators=[DataRequired()], choices=["yes", "no"]
    )
