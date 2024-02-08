from wtforms import Form, validators, IntegerField


class CreatePaymentOtpForm(Form):
    OTP_code_1 = IntegerField('',[validators.length(max=1), validators.DataRequired()])
    OTP_code_2 = IntegerField('',[validators.length(max=1), validators.DataRequired()])
    OTP_code_3 = IntegerField('',[validators.length(max=1), validators.DataRequired()])
    OTP_code_4 = IntegerField('',[validators.length(max=1), validators.DataRequired()])
    OTP_code_5 = IntegerField('',[validators.length(max=1), validators.DataRequired()])
    OTP_code_6 = IntegerField('',[validators.length(max=1), validators.DataRequired()])

def GenerateOTP():
    import random

    OTP = ''
    for i in range(6):
        OTP += str(random.randint(0,9))
    return OTP

def SendEmail(otp, receiver):
    from email.message import EmailMessage
    import ssl
    import smtplib

    email_sender = 'greenuniversitypayment@gmail.com'
    email_password = 'calb ujxv htrk jlab'
    email_receiver = receiver

    subject = 'Email Verification'
    body = 'The code is ' + otp

    msg = EmailMessage()
    msg['From'] = email_sender
    msg['To'] = email_receiver
    msg['subject'] = subject
    msg.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, msg.as_string())
