from wtforms import Form, validators, IntegerField

class CreatePaymentOtpForm(Form):
    OTP_code_1 = IntegerField('',[validators.length(max=1), validators.DataRequired()])
    OTP_code_2 = IntegerField('',[validators.length(max=1), validators.DataRequired()])
    OTP_code_3 = IntegerField('',[validators.length(max=1), validators.DataRequired()])
    OTP_code_4 = IntegerField('',[validators.length(max=1), validators.DataRequired()])
    OTP_code_5 = IntegerField('',[validators.length(max=1), validators.DataRequired()])
    OTP_code_6 = IntegerField('',[validators.length(max=1), validators.DataRequired()])