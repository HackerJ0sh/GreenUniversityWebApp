from wtforms import Form, StringField, FileField, TextAreaField, SelectMultipleField, validators
from flask_wtf.file import FileAllowed, FileRequired


class CreateBlogForm(Form):
    post_name = StringField('Subject', [validators.Length(min=1, max=150), validators.DataRequired()])
    image = FileField('Image File (Optional)', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
    post_content = TextAreaField('Description', [validators.Length(min=1, max=2000), validators.DataRequired()])
    category = SelectMultipleField('Category(ies)', choices=
    [('REC', 'Recycling'), ('SSB', 'Sustainability'),
     ('BIZ', 'Business'), ('H20', 'Water'), ('CUL', 'Cultural'), ('ETC', 'Other')],
    validators=[validators.DataRequired()], default='')


class SearchBlogForm(Form):
    post_name = StringField('Blog Title: ', [validators.Length(min=0, max=150)])
