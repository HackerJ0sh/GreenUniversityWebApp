from wtforms import Form, StringField, RadioField, SelectField, validators, PasswordField, BooleanField
from wtforms.fields import EmailField

class UpdateUserForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    username = StringField('Username', [validators.Length(min=1, max=150), validators.DataRequired()])
    password = StringField('Password', [validators.DataRequired(),validators.Length(min=8)])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()],
                         choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    security_question = StringField('Security Question', [validators.Length(min=1, max=150), validators.DataRequired()])
    security_answer = StringField('Security Answer', [validators.Length(min=1, max=150), validators.DataRequired()])
    account_status = RadioField('Account Status', choices=[('L', 'Locked'), ('U', 'Unlocked')], default='U')
    account_type = RadioField('Account Type', choices=[('C', 'Customer'), ('S', 'Staff')], default='C')
class CreateUserForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    username = StringField('Username', [validators.Length(min=1, max=150), validators.DataRequired()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.Length(min=8),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    security_question = StringField('Security Question', [validators.Length(min=1, max=150), validators.DataRequired()])
    security_answer = StringField('Security Answer', [validators.Length(min=1, max=150), validators.DataRequired()])
    account_status = RadioField('Account Status', choices=[('L', 'Locked'), ('U', 'Unlocked')], default='U')
    account_type = RadioField('Account Type', choices=[('C', 'Customer'), ('S', 'Staff')], default='C')

class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=1, max=150), validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])

class ResetUserForm(Form):
    username = StringField('Username', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])

class SecurityForm(Form):
    security_answer = StringField('Security Answer')

class ChangePasswordForm(Form):
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.Length(min=8),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')