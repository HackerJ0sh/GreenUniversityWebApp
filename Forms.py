from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, IntegerField, DecimalField, FileField, SubmitField
from wtforms.fields import EmailField, DateField 
from flask_wtf.file import FileAllowed, FileRequired


class CreateUserForm(Form):
    first_name = StringField('Product Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = DecimalField('Product Price', [validators.DataRequired()])
    gender = SelectField('Category', [validators.DataRequired()], choices=[('', 'Select'), ('Shirt', 'Shirt'), ('Pants', 'Pants')], default='')
    membership = RadioField('Size', choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large')], default='S')   
    remarks = TextAreaField('Remarks',[validators.Optional()],)
    quantity = IntegerField('Quantity', [validators.NumberRange(min=1, max=10000)])
    image = FileField('Image (only jpg, jpeg, png format is allowed)', validators=[FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField('Submit')



