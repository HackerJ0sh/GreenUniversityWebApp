from wtforms import Form, StringField, TextAreaField, SelectMultipleField, validators


class CreateReportForm(Form):
    reported_account = StringField("Reported Blog ID", [validators.Length(min=1, max=150), validators.DataRequired()])
    report_subjects = SelectMultipleField('Reasons for Report', choices=
    [('1', 'Unrelated to the environment'), ('2', 'Harassment and bullying'),
     ('3', 'Illegal content'), ('4', 'Plagiarism'), ('5', 'Misinformative or disinformative')],
    validators=[validators.DataRequired()], default='')
    report_reason = TextAreaField('Describe in detail the situation'
    ' so that our staff can help you resolve the issue promptly.',
    [validators.Length(min=1, max=2000), validators.DataRequired()])


