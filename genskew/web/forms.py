from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, StringField
from wtforms.validators import DataRequired


class NewTabForm(FlaskForm):
    file = FileField('File: ', validators=[DataRequired()])
    title = StringField('Title: ', render_kw={"placeholder": "Type optional title here..."})
    submit = SubmitField('Upload File & Plot Sequence')
