from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, IntegerField, DecimalField, FileField, SubmitField
from wtforms.fields import EmailField, DateField 
from flask_wtf.file import FileAllowed, FileRequired




class CreateProductForm(Form):
    product_name = StringField('Product Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    product_price = DecimalField('Product Price', [validators.DataRequired()], places=2, rounding=None)
    product_category = StringField('Category', [validators.Length(min=1, max=15), validators.DataRequired()]) 
    remarks = TextAreaField('Description',[validators.DataRequired()],)
    quantity = IntegerField('Quantity', [validators.NumberRange(min=1, max=10000)])
    image = FileField('Image (only jpg and png format is allowed)', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Submit')

