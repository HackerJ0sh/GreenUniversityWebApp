from flask import * 
from PaymentForm import CreatePaymentForm
import shelve
from dataClasses.Payment import PaymentInfo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

@app.route('/')
def home():
    return render_template('home.html')

# @app.route('/payment/<int:id>', methods=["POST", "GET"])
@app.route('/payment', methods=["POST", "GET"])
def payment():
    create_payment_form = CreatePaymentForm(request.form)
    if request.method == "POST" and create_payment_form.validate():
        payment_dict = {}
        db = shelve.open('payment.db', 'c')
        try:
            payment_dict = db['Payments']
        except: 
            print('Error in opening the file')

        payment_info = PaymentInfo(
            address_line_1=create_payment_form.address_line_1.data,
            address_line_2=create_payment_form.address_line_2.data,
            country=create_payment_form.country.data,
            postal_code=create_payment_form.postal_code.data,
            expiry_date_month=create_payment_form.expiry_date_month.data,
            expiry_date_year=create_payment_form.expiry_date_year.data,
            cvv=create_payment_form.cvv.data,
            credit_card_holder=create_payment_form.card_holder_name.data,
            credit_card_number=create_payment_form.credit_card_number.data,
            remember=create_payment_form.remember.data
        )

        # add code: add all the payment_info objects to the user class attribute called transaction=[], this allows the users to see all their transactions

        # saves the payment details if remember is true
        if create_payment_form.remember.data:
            payment_dict[payment_info.get_id()] = payment_info
            db['Payments'] = payment_dict
        
        db.close()

        # add email code verification / 2FA / use email api 

        flash('Payment Successful', 'info')
        return redirect(url_for('payment_successful'))
    return render_template('paymentForm.html', form=create_payment_form)

# @app.route('/payment/<int:id>/successful')
@app.route('/payment/successful')
def payment_successful():
    return render_template('paymentSuccess.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)
