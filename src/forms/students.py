from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    BooleanField,
    TextAreaField,
    SelectField,
    DateTimeField,
    IntegerField,
)
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


class AddStudentSessionForm(FlaskForm):
    date = DateTimeField("Date", validators=[DataRequired()])
    duration = IntegerField("Duration", validators=[DataRequired()])
    session_type = SelectField(
        "Session Type",
        validators=[DataRequired()],
        choices=["intro", "inception", "middle", "end", "prep", "no-show", "other"],
    )
    project = SelectField(
        "Project",
        validators=[DataRequired()],
        choices=["UCFD", "IFD", "DCD", "FSFwD", "other"],
    )
    summary = TextAreaField("Summary", validators=[DataRequired()])
    progress = SelectField(
        "Student Progress",
        validators=[DataRequired()],
        choices=["poor", "average", "excellent"],
    )
    concerns = TextAreaField("Concerns")
    personal_notes = TextAreaField("Personal Notes")
