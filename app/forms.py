from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields import DateTimeLocalField

class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    start_time = DateTimeLocalField('Start Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    end_time = DateTimeLocalField('End Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Save')

class ResourceForm(FlaskForm):
    resource_name = StringField('Resource Name', validators=[DataRequired()])
    resource_type = SelectField('Resource Type', choices=[('room','Room'),('instructor','Instructor'),('equipment','Equipment')], validators=[DataRequired()])
    submit = SubmitField('Save')

class AllocationForm(FlaskForm):
    event = SelectField('Event', coerce=int, validators=[DataRequired()])
    resources = SelectMultipleField('Resources (Ctrl/Command+click to select multiple)', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Allocate')
