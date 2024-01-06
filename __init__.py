from flask import * 
from PaymentForm import CreatePaymentForm, UpdatePaymentForm
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

        # TODO: add email code verification / 2FA / use email api 

        flash('Payment Successful', 'info')
        return redirect(url_for('payment_successful'))
    return render_template('paymentForm.html', form=create_payment_form)

# @app.route('/payment/<int:id>/successful')
@app.route('/payment/successful')
def payment_successful():
    return render_template('paymentSuccess.html')


@app.route('/payment/update', methods=["POST", "GET"])
def payment_update():
    update_payment_form = UpdatePaymentForm(request.form)
    if request.method == "POST" and update_payment_form.validate():
        payment_dict ={}
        db = shelve.open('payment.db', 'w')
        payment_dict = db['Payments']

        # TODO: get id from user payment info object
        payment_info = payment_dict[1]

        payment_info.set_address_line_1(update_payment_form.address_line_1.data)
        payment_info.set_address_line_2(update_payment_form.address_line_2.data)
        payment_info.set_postal_code(update_payment_form.postal_code.data)
        payment_info.set_country(update_payment_form.country.data)
        payment_info.set_cvv(update_payment_form.cvv.data)
        payment_info.set_expiry_date_year(update_payment_form.expiry_date_year.data)
        payment_info.set_expiry_date_month(update_payment_form.expiry_date_month.data)
        payment_info.set_credit_card_holder(update_payment_form.card_holder_name.data)
        payment_info.set_credit_card_number(update_payment_form.credit_card_number.data)

        db["Payments"] = payment_dict
        db.close()

        flash('Successfully Updated Payment Information')
        return redirect(url_for('home'))
    else: 
        # TODO: find the payment information associated with the user | add code
        return render_template('paymentUpdate.html', form=update_payment_form)


@app.route('/payment/delete')
def payment_delete():
    # retrieve the payment_info object from user class and delete it.
    payment_dict = {}
    try:
        db = shelve.open('payment.db')
    except IOError:
        flash('Please create your payment information first')
        return redirect(url_for('home'))
    
    payment_dict = db['Payments']
    payment_dict.pop(1)

    db['Payments'] = payment_dict
    db.close()

    flash('Successfully deleted payment information')
    return redirect(url_for('view_payment'))
    

@app.route('/payment/view')
def view_payment():
    payment_dict = {}
    db = shelve.open('payment.db', 'r')
    payment_dict = db['Payments']

    db.close()
    payment_info = payment_dict[1]

    return render_template('paymentView.html', payment_info=payment_info)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
