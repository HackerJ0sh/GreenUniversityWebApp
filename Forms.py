from wtforms import Form, RadioField, TextAreaField, validators
class CreateFeedbackForm(Form):
#To change attributes in Create Feedback HTML
    membership = RadioField('Satisfaction Level', choices=[('G', 'Good'), ('N', 'Neutral'), ('B', 'Bad')], default='F',
    render_kw={'class': 'custom-radio-input'}
)

    remarks = TextAreaField('Feedback', [validators.Optional(), validators.length(min=1, max=500)])