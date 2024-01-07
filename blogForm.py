from wtforms import Form, StringField, FileField, TextAreaField, SelectMultipleField, validators


class CreateBlogForm(Form):
    post_name = StringField('Subject', [validators.Length(min=1, max=150), validators.DataRequired()])
    image = FileField('Image File', [validators.regexp(u'^.+\.jpg$'), validators.Optional()])
    post_content = TextAreaField('Description', [validators.Length(min=1, max=2000), validators.DataRequired()])
    category = SelectMultipleField(u'Category(ies)', choices=
    [('REC', 'Recycling'), ('SSB', 'Sustainability'), ('BIZ', 'Business'), ('H20', 'Water'), ('CUL', 'Cultural')],
    validators=[validators.DataRequired()])


