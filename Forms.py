from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, IntegerField
from wtforms.fields import EmailField, DateField

class CreateUserForm(Form):
    first_name = StringField('Product Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Product Price', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Category', [validators.DataRequired()], choices=[('', 'Select'), ('Shirt', 'Shirt'), ('Pants', 'Pants')], default='')
    membership = RadioField('Size', choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large')], default='S')
    img_url = StringField("img_url", [validators.DataRequired()])
    remarks = TextAreaField('Remarks',[validators.Optional()],)
    quantity = IntegerField('Quantity', [validators.NumberRange(min=1, max=500)])

class CreateCustomerForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    date_joined = DateField('Date Joined', format='%Y-%m-%d')
    address = TextAreaField('Mailing Address', [validators.length(max=200), validators.DataRequired()])
    membership = RadioField('Membership', choices=[('F', 'Fellow'), ('S', 'Senior'), ('P', 'Professional')], default='F')
    remarks = TextAreaField('Remarks', [validators.Optional()])
