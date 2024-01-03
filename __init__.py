from flask import * 
from PaymentForm import CreatePaymentForm
import shelve
from dataClasses.Payment import PaymentInfo

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/payment/<int:id>', methods=["POST", "GET"])
def payment():
    create_payment_form = CreatePaymentForm(request.form)
    if request.method == "POST" and create_payment_form.validate():
        payment_dict = {}
        db = shelve.open('payment.db', 'c')
        try:
            payment_dict = db['Payments']
        except: 
            print('Error in opening the file')

        payment_info = PaymentInfo(create_payment_form.address_line_1.data, create_payment_form.address_line_2)
        # continue adding the fields
    

if __name__ == "__main__":
    app.run(debug=True, port=5000)
