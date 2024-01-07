from wtforms import Form, StringField, RadioField, SelectField, validators
from wtforms.fields import EmailField

class CreateUserForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    username = StringField('Username', [validators.Length(min=1, max=150), validators.DataRequired()])
    password = StringField('Password', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    security_question = StringField('Security Question', [validators.Length(min=1, max=150), validators.DataRequired()])
    security_answer = StringField('Security Answer', [validators.Length(min=1, max=150), validators.DataRequired()])
    account_status = RadioField('Account Status', choices=[('L', 'Locked'), ('U', 'Unlocked')], default='U')
    account_type = RadioField('Account Type', choices=[('C', 'Customer'), ('S', 'Staff')], default='C')
