from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, AnyOf, URL, Optional


class AnswerForm(Form):

    # text field
    answer = StringField('Type your answer here', validators = [DataRequired()])
    submit = SubmitField('Submit')


class QuestionForm(Form):

    title = StringField('Question title', validators = [DataRequired()])
    body = StringField('Question detail ', validators = [DataRequired()])
    submit = SubmitField('Submit')

class SearchForm(Form):

    search_body = StringField('Search for questions using any keywords (e.g., What language should I study first ?)', validators = [DataRequired()])
    submit = SubmitField('Search')
