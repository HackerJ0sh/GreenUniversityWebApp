from wtforms import Form, StringField, FileField, TextAreaField, SelectMultipleField, validators
from flask_wtf.file import FileAllowed, FileRequired


class CreateBlogForm(Form):
    post_name = StringField('Subject', [validators.Length(min=1, max=150), validators.DataRequired()])
    image = FileField('Image File', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
    post_content = TextAreaField('Description', [validators.Length(min=1, max=2000), validators.DataRequired()])
    category = SelectMultipleField('Category(ies)', choices=
    [('REC', 'Recycling'), ('SSB', 'Sustainability'),
     ('BIZ', 'Business'), ('H20', 'Water'), ('CUL', 'Cultural')],
    validators=[validators.DataRequired()], default='')


class SearchBlogForm(Form):
    account_id = StringField('Created by: ', [validators.Length(min=0, max=150)])
    blog_id = StringField('Blog ID: ', validators=[validators.Length(min=0, max=15)])
    blog_category = SelectMultipleField(label='', choices=
    [('REC', 'Recycling'), ('SSB', 'Sustainability'),
     ('BIZ', 'Business'), ('H20', 'Water'), ('CUL', 'Cultural')], default='')
