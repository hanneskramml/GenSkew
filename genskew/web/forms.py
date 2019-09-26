from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, StringField
from wtforms.validators import DataRequired


# TODO: replace with plain HTML5
class NewTabForm(FlaskForm):
    file = FileField('File: ', validators=[DataRequired()])
    title = StringField('Title: ', render_kw={"placeholder": "Enter optional title..."})
    submit = SubmitField('Upload File & Plot Sequence')
