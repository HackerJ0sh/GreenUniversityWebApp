from flask import *
from fpdf import FPDF
from Charts import Charts
from PaymentForm import CreatePaymentForm, UpdatePaymentForm
from PaymentOtpForm import CreatePaymentOtpForm, SendEmail, GenerateOTP
import shelve, Product , random , Account_Class, Feedback
from Payment import PaymentInfo
from ProductForm import CreateProductForm
from flask_wtf.file import FileAllowed
from Account_Forms import CreateUserForm,LoginForm, UpdateUserForm, ResetUserForm, SecurityForm, ChangePasswordForm
from Forms import CreateFeedbackForm
from functions import *
from blogForm import *
from formClasses import *
from reportForm import CreateReportForm
from random import randint
import os
from flask_login import LoginManager, current_user, logout_user, login_user, login_required
import datetime
import json
from pdfCreator import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['UPLOAD_FOLDER'] = 'static/files'
allowed_extensions_list = ['jpg', 'png', 'jpeg', '']

#
#Joshua routing
#

# Get Data Route 
@app.route('/getChartData', methods=["POST", "GET"])
def get_chart_data():
    count = []
    chart_data_dict = {}

    db = shelve.open('ChartData.db', 'r')
    chart_data_dict = db['ChartData']
    db.close()

    count = [chart_data_dict['total_kitchen'], chart_data_dict['total_lifestyle'], chart_data_dict['total_bathroom']]

    data = {
        "count": count
    }
    return data

# dashboard route 
@app.route('/staff/home')
def staff_home():
    # get total products
    products_dict = {}
    db_product = shelve.open('product.db', 'r')
    products_dict = db_product['Products']
    db_product.close()
    
    
    products_list = []
    for key in products_dict:
        product = products_dict.get(key)
        products_list.append(product)

    # get total customers
    users_dict = {}
    db_user = shelve.open('user.db', 'r')
    users_dict = db_user['Users']
    db_user.close()

    users_list = []
    for key2 in users_dict:
        user = users_dict.get(key2)
        users_list.append(user)

    # get total orders and total earnings
    chart_data_dict = {}
    db_chart_data = shelve.open('ChartData.db', 'r')
    chart_data_dict = db_chart_data['ChartData']

    total_orders = chart_data_dict['total_orders']
    total_earnings = chart_data_dict['total_earnings']
    
    staff_name = session['staff_name']

    return render_template('staffDashboard.html', total_cust=len(users_list), staff_name=staff_name, total_products=len(products_list), total_earnings=total_earnings, total_orders=total_orders)

@app.route('/')
def home():
    return render_template('home.html')

# @app.route('/payment/<int:id>', methods=["POST", "GET"])
@app.route('/payment', methods=["POST", "GET"])
# @login_required
def payment():
    create_payment_form = CreatePaymentForm(request.form)

    try: 
        id = session['customer_id']
        payment_dict = {}
        db = shelve.open('payment.db', 'r')
        payment_dict = db['Payments']
        cust_payment_info = payment_dict[id]

        if cust_payment_info.get_remember():
            session['email'] = cust_payment_info.get_email()
            return redirect(url_for('payment_otp'))
    except:
        print('Customer did not create payment information')
        
    if request.method == "POST" and create_payment_form.validate():

        payment_dict = {}
        db = shelve.open('payment.db', 'c')
        try:
            payment_dict = db['Payments']
        except: 
            print('Error in opening the file')

        session['email'] = create_payment_form.email.data
        id = session['customer_id']

        payment_info = PaymentInfo(
            full_name=create_payment_form.full_name.data,
            phone_number=create_payment_form.phone_number.data,
            email=create_payment_form.email.data,
            address_line_1=create_payment_form.address_line_1.data,
            address_line_2=create_payment_form.address_line_2.data,
            country=create_payment_form.country.data,
            postal_code=create_payment_form.postal_code.data,
            expiry_date_month=create_payment_form.expiry_date_month.data,
            expiry_date_year=create_payment_form.expiry_date_year.data,
            cvv=create_payment_form.cvv.data,
            credit_card_holder=create_payment_form.card_holder_name.data,
            credit_card_number=create_payment_form.credit_card_number.data,
            remember=create_payment_form.remember.data, 
            donation=create_payment_form.donation.data
        )

        # add code: add all the payment_info objects to the user class attribute called transaction=[], this allows the users to see all their transactions
        payment_info.set_user_id(id)

        # saves the payment details if remember is true
        if create_payment_form.remember.data:
            payment_dict[payment_info.get_user_id()] = payment_info
            db['Payments'] = payment_dict
        
            db.close()
 
        flash('Please Verify Your Email To Proceed')

        return redirect(url_for('payment_otp'))
    
    userid = session["customer_id"]
    cart_dict = {}
    db = shelve.open('shoppingcart.db','r')
    cart_dict = db[f'{userid}']
    db.close()

    cart_list = []
    total_price = 0
    for key in cart_dict:
        product = cart_dict.get(key)
        cart_list.append(product)
        price = product.get_product_price()
        total_price += float(price)

    total_price = f"{total_price:.2f}"

    return render_template('paymentForm.html', form=create_payment_form, cart_list=cart_list, total=total_price, cart_count=len(cart_list))

# @app.route('/payment/<int:id>/successful')
@app.route('/payment/successful')
# @login_required
def payment_successful():
    id = session['customer_id']

    # get total price 
    db = shelve.open('shoppingcart.db','r')
    cart_dict = db[f'{id}']
    db.close()

    total_price = 0
    for key in cart_dict:
        product = cart_dict.get(key)
        price = product.get_product_price()
        total_price += float(price)

    total_price = f"{total_price:.2f}"

    # create a new DB to grab important data analysis datas for the KPIs 
    chart_data_dict = {}
    try: 
        db_chart_data = shelve.open('ChartData.db', 'r')
        db_chart_data['ChartData'] = chart_data_dict
    except: 
        db_chart_data = shelve.open('ChartData.db', 'c')
        chart_data_dict = db_chart_data['ChartData']

    if 'total_earnings' not in chart_data_dict:
        chart_data_dict['total_earnings'] = 0.0  
    if 'total_orders' not in chart_data_dict:
        chart_data_dict['total_orders'] = 0
    if 'total_kitchen' not in chart_data_dict:
        chart_data_dict['total_kitchen'] = 0
    if 'total_lifestyle' not in chart_data_dict:
        chart_data_dict['total_lifestyle'] = 0
    if 'total_bathroom' not in chart_data_dict:
        chart_data_dict['total_bathroom'] = 0

    # get chart data
    db = shelve.open('shoppingcart.db','r')
    cart_dict = db[f'{id}']
    db.close()

    for key in cart_dict:
        product = cart_dict.get(key)
        category = product.get_product_category()

        if category == 'Kitchen':
            chart_data_dict['total_kitchen'] += 1
        elif category == 'Lifestyle':
            chart_data_dict['total_lifestyle'] += 1
        elif category == 'Bathroom':
            chart_data_dict['total_bathroom'] += 1




    chart_data_dict['total_earnings'] += float(total_price)
    chart_data_dict['total_orders'] += 1

    db_chart_data['ChartData'] = chart_data_dict
    db_chart_data.close()



    db = shelve.open('shoppingcart.db', 'w')
    products_dict = db[f'{id}']
    products_dict.clear()

    db[f'{id}'] = products_dict
    db.close()

    return render_template('paymentSuccessful.html')


@app.route('/payment/update', methods=["POST", "GET"])
# @login_required
def payment_update():
    update_payment_form = UpdatePaymentForm(request.form)
    if request.method == "POST" and update_payment_form.validate():
        payment_dict ={}
        try:
            db = shelve.open('payment.db', 'w')
            payment_dict = db['Payments']
        except:
            flash('Please Create Your Payment Information First')
            return redirect(url_for('payment'))

        # TODO: get id from user payment info object
        id = session['customer_id']
        payment_info = payment_dict[id]

        payment_info.set_full_name(update_payment_form.full_name.data)
        payment_info.set_phone_number(update_payment_form.phone_number.data)
        payment_info.set_email(update_payment_form.email.data)
        payment_info.set_address_line_1(update_payment_form.address_line_1.data)
        payment_info.set_address_line_2(update_payment_form.address_line_2.data)
        payment_info.set_postal_code(update_payment_form.postal_code.data)
        payment_info.set_country(update_payment_form.country.data)
        payment_info.set_cvv(update_payment_form.cvv.data)
        payment_info.set_expiry_date_year(update_payment_form.expiry_date_year.data)
        payment_info.set_expiry_date_month(update_payment_form.expiry_date_month.data)
        payment_info.set_credit_card_holder(update_payment_form.card_holder_name.data)
        payment_info.set_credit_card_number(update_payment_form.credit_card_number.data)
        payment_info.set_donation(update_payment_form.donation.data)

        db['Payments'] = payment_dict
        db.close()

        flash('Successfully Updated Payment Information')
        return redirect(url_for('view_payment'))
    else: 
        # TODO: find the payment information associated with the user | add code
        return render_template('paymentUpdate.html', form=update_payment_form)


@app.route('/payment/OTP', methods=["POST", "GET"])
# @login_required
def payment_otp():
    create_paymentOTP_form = CreatePaymentOtpForm(request.form)
    email_receiver = session['email']

    if request.method == "GET":  
        OTP = GenerateOTP()
        SendEmail(otp=OTP, receiver=email_receiver) 
        session['OTP'] = OTP

        return render_template('paymentOTP.html', form=create_paymentOTP_form, email=email_receiver)
    else:
        form_OTP = str(create_paymentOTP_form.OTP_code_1.data) + str(create_paymentOTP_form.OTP_code_2.data) + str(create_paymentOTP_form.OTP_code_3.data) + str(create_paymentOTP_form.OTP_code_4.data) + str(create_paymentOTP_form.OTP_code_5.data) + str(create_paymentOTP_form.OTP_code_6.data)
        print(form_OTP)
        OTP = session['OTP']
        if form_OTP == OTP:
            flash('Payment Successful')
            
            del session['OTP']
            return redirect(url_for('payment_successful'))
        else:
            flash('The OTP you entered does not match')
            return redirect(url_for('payment_otp'))


@app.route('/payment/delete')
# @login_required
def payment_delete():
    # retrieve the payment_info object from user class and delete it.
    payment_dict = {}
    id = session['customer_id']
    try:
        db = shelve.open('payment.db')

        payment_dict = db['Payments']
        payment_dict.pop(id)

        db['Payments'] = payment_dict
        db.close()
    except:
        flash('Please Create Your Payment Information First')
        return redirect(url_for('payment'))
    
    flash('Successfully deleted payment information')
    return redirect(url_for('view_payment'))
    

@app.route('/payment/view')
# @login_required
def view_payment():
    payment_dict = {}
    try:
        db = shelve.open('payment.db', 'r')
        payment_dict = db['Payments']
        db.close()
    except:
        flash('Please Create Your Payment Information First')
        return redirect(url_for('payment'))

    try:
        id = session['customer_id']
        payment_info = payment_dict[id]
    except:
        payment_info = None

    return render_template('paymentView.html', payment_info=payment_info)

@app.route('/aboutUs')
def about_us():
    return render_template('aboutUs.html')

@app.route('/AboutUs')
def about_usReal():
    return render_template('aboutUsReal.html')


@app.route('/faq')
def faq():
    return render_template('faq.html')



#
# bing routing 
#

@app.route('/store')
def store():
    products_dict = {}
    db = shelve.open('product.db', 'r')
    products_dict = db['Products']
    db.close()
    
    
    products_list = []
    for key in products_dict:
        product = products_dict.get(key)
        products_list.append(product)
        
        

    return render_template('store.html', count=len(products_list), products_list=products_list)

@app.route('/<int:id>/info', methods=["POST", "GET"])
def info(id):
    products_dict = {}
    db = shelve.open('product.db', 'r')
    products_dict = db['Products']
    db.close()

    products_list = []
    
    product = products_dict.get(id)
    products_list.append(product)
    
    return render_template('info.html', products_list=products_list)

@app.route('/cart')
def cart():
    userid = session["customer_id"]
    cart_dict = {}
    db = shelve.open('shoppingcart.db','r')
    cart_dict = db[f'{userid}']
    db.close()

    cart_list = []
    total_price = 0
    for key in cart_dict:
        product = cart_dict.get(key)
        cart_list.append(product)
        price = product.get_product_price()
        total_price += float(price)

    total_price = f"{total_price:.2f}"
        
    return render_template('cart.html', cartcount=len(cart_list), cart_list=cart_list,total=total_price,userid=userid)

@app.route('/<int:id>/add_to_cart', methods=["POST", "GET"])
def add_to_cart(id):

    userid = session["customer_id"]
    products_dict = {}
    db = shelve.open('product.db', 'r')
    products_dict = db['Products']
    product = products_dict.get(id)
    db.close()

    cart_dict = {}
    db2 = shelve.open('shoppingcart.db','c')

    cart_dict = db2[f'{userid}']
    cart_dict[id] = product
    db2[f'{userid}'] = cart_dict
    db.close()
    
    return redirect(url_for('cart'))

        
@app.route('/<int:id>/remove_from_cart', methods=['POST'])
def remove_from_cart(id):
    userid = session["customer_id"]
    products_dict = {}
    db = shelve.open('shoppingcart.db', 'w')
    products_dict = db[f'{userid}']

    products_dict.pop(id)

    db[f'{userid}'] = products_dict
    db.close()

    return redirect(url_for('cart'))
        

         
    





@app.route('/invalidfile')
def invalid_file():
    return render_template('invalidfile.html')



@app.route('/createProduct', methods=['GET', 'POST'])
def create_product():
    create_product_form = CreateProductForm(request.form)
    allowed_extensions_list = ['jpg','png']  
    if request.method == 'POST' and create_product_form.validate():
        products_dict = {}
        db = shelve.open('product.db', 'c')

        try:
            products_dict = db['Products']
        except:
            print("Error in retrieving Products from product.db.")

        
        img = request.files.getlist('image')[0]
        if img.filename.split(".")[-1].lower() not in allowed_extensions_list:
            return redirect(url_for('invalid_file'))
        else:
            product = Product.Product(create_product_form.product_name.data, 
                         create_product_form.product_price.data, 
                         create_product_form.product_category.data, 
                         
                         create_product_form.remarks.data, 
                         create_product_form.quantity.data)
            products_dict[product.get_product_id()] = product
            db['Products'] = products_dict

            db.close()
            img.save(f'./static/images/{product.get_product_name()}.{img.filename.split(".")[-1]}')
            
        # assign a file name to the saved image
        

        return redirect(url_for('retrieve_products'))
    return render_template('createProduct.html', form=create_product_form)

@app.route('/retrieveInventory')
def retrieve_products():
    products_dict = {}
    db = shelve.open('product.db', 'r')
    products_dict = db['Products']
    db.close()

    
    products_list = []
    for key in products_dict:
        product = products_dict.get(key)
        products_list.append(product)
        
    return render_template('retrieveProducts.html', count=len(products_list), products_list=products_list,)


@app.route('/updateProduct/<int:id>/', methods=['GET', 'POST'])
def update_product(id):
    update_product_form = CreateProductForm(request.form)
    if request.method == 'POST' and update_product_form.validate():
        products_dict = {}
        db = shelve.open('product.db', 'w')
        products_dict = db['Products']

        product = products_dict.get(id)
        product.set_product_name(update_product_form.product_name.data)
        product.set_product_price(update_product_form.product_price.data)
        product.set_product_category(update_product_form.product_category.data)
        
        product.set_remarks(update_product_form.remarks.data)
        product.set_quantity(update_product_form.quantity.data)

        db['Products'] = products_dict
        db.close()
        

        return redirect(url_for('retrieve_products'))
    else:
        products_dict = {}
        db = shelve.open('product.db', 'r')
        products_dict = db['Products']
        db.close()

        product = products_dict.get(id)
        update_product_form.product_name.data = product.get_product_name()
        update_product_form.product_price.data = product.get_product_price()
        update_product_form.product_category.data = product.get_product_category()
        
        update_product_form.remarks.data = product.get_remarks()
        update_product_form.quantity.data = product.get_quantity()

        return render_template('updateProduct.html', form=update_product_form)


@app.route('/deleteProduct/<int:id>', methods=['POST'])
def delete_product(id):
    products_dict = {}
    db = shelve.open('product.db', 'w')
    products_dict = db['Products']

    products_dict.pop(id)

    db['Products'] = products_dict
    db.close()

    return redirect(url_for('retrieve_products'))

#
#kendrick routing
#
@app.route("/cust_home", methods=['GET', 'POST'])
#@login_required
def cust_homepage():
    id = session["customer_id"]
    users_dict = {}
    db = shelve.open('user.db', 'r')
    users_dict = db['Users']
    db.close()
    name = users_dict[id].get_name()
    return render_template("customerHomepage.html", name=name, id=id)

@app.route("/staff_home", methods=['GET', 'POST'])
#@login_required
def staff_homepage():
    id = session["customer_id"]
    users_dict = {}
    db = shelve.open('user.db', 'r')
    users_dict = db['Users']
    db.close()
    name = users_dict[id].get_name()
    session["staff_name"] = name
    return redirect(url_for('staff_home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    register_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and register_user_form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'c')

        try:
            users_dict = db['Users']
        except:
            print("Error in retrieving Users from user.db.")

        user = Account_Class.User(register_user_form.name.data, register_user_form.username.data,
                                  register_user_form.password.data, register_user_form.email.data,
                                  register_user_form.gender.data, register_user_form.security_question.data,
                                  register_user_form.security_answer.data, register_user_form.account_status.data, register_user_form.account_type.data)
        users_dict[user.get_user_id()] = user
        db['Users'] = users_dict

        db.close()

        return redirect(url_for('login'))
    return render_template('signup.html', form=register_user_form, title="registration page")

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_user_form = LoginForm(request.form)
    if request.method == 'POST' and login_user_form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'r')
        users_dict = db['Users']
        db.close()
        error_login = 0
        error_lock = 0
        for key in users_dict:
            if login_user_form.username.data == users_dict[key].get_username():
                password = users_dict[key].get_password()
                if login_user_form.password.data == password:
                    if users_dict[key].get_account_status() == "L":
                        error_lock = error_lock + 1
                        break
                    elif users_dict[key].get_account_type() == "S":
                        session['customer_email'] = users_dict[key].get_email()
                        session['customer_id'] = users_dict[key].get_user_id()
                        session['customer_username'] = users_dict[key].get_username()
                        return redirect(url_for('staff_homepage', id=users_dict[key].get_user_id()))
                    else:
                        session['customer_email'] = users_dict[key].get_email()
                        session['customer_id'] = users_dict[key].get_user_id()
                        session['customer_username'] = users_dict[key].get_username()
                        return redirect(url_for('cust_homepage', id=users_dict[key].get_user_id()))
                else:
                    error_login = error_login + 1

            else:
                error_login = error_login + 1
        if error_login > 0:
            flash("Wrong Username or Password", "default")
        if error_lock > 0:
            flash("Your Account is locked. Contact an admin.", "locked")


    return render_template('login.html', form=login_user_form, title = "Login Page")

@app.route('/contactUs')
def contact_us():
    return render_template('contactUs.html')

@app.route('/createUser', methods=['GET', 'POST'])
def create_user():
    create_user_form = CreateUserForm(request.form)
    users_dict = {}
    db = shelve.open('user.db', 'r')
    users_dict = db['Users']
    db.close()
    repeat = 0
    for key in users_dict:
        if create_user_form.username.data == users_dict[key].get_username():
            repeat = 1
            flash("Username is taken", "username")
            break
    for key in users_dict:
        if create_user_form.email.data == users_dict[key].get_email():
            repeat = 1
            flash("Email is taken", "email")
            break
    if request.method == 'POST' and create_user_form.validate() and repeat == 0:
        users_dict = {}
        db = shelve.open('user.db', 'c')

        try:
            users_dict = db['Users']
        except:
            print("Error in retrieving Users from user.db.")

        user = Account_Class.User(create_user_form.name.data, create_user_form.username.data, create_user_form.password.data, create_user_form.email.data, create_user_form.gender.data, create_user_form.security_question.data, create_user_form.security_answer.data, create_user_form.account_status.data, create_user_form.account_type.data)
        users_dict[user.get_user_id()] = user
        db['Users'] = users_dict

        db.close()

        return redirect(url_for('retrieve_users'))
    return render_template('create_account.html', form=create_user_form, id=id)

@app.route('/retrieveUsers')
def retrieve_users():
    users_dict = {}
    db = shelve.open('user.db', 'r')
    users_dict = db['Users']
    db.close()

    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)

    return render_template('retrieve_account.html', count=len(users_list), users_list=users_list)

@app.route('/updateUser/<int:id>/', methods=['GET', 'POST'])
def update_user(id):
    update_user_form = UpdateUserForm(request.form)
    users_dict = {}
    db = shelve.open('user.db', 'r')
    users_dict = db['Users']
    db.close()
    repeat = 0
    username = users_dict[id].get_username()
    email = users_dict[id].get_email()
    for key in users_dict:
        if update_user_form.username.data == users_dict[key].get_username():
            if update_user_form.username.data == username:
                repeat = repeat + 0
            else:
                repeat = repeat + 1
                flash("Username is taken (Revert back to original)", "username")
            break
    for key in users_dict:
        if update_user_form.email.data == users_dict[key].get_email():
            if update_user_form.email.data == email:
                repeat =  repeat + 0
            else:
                repeat =  repeat + 1
                flash("Email is taken (Revert back to original)", "email")
                break
    if request.method == 'POST' and update_user_form.validate() and repeat < 1:
        users_dict = {}
        db = shelve.open('user.db', 'w')
        users_dict = db['Users']

        user = users_dict.get(id)
        user.set_name(update_user_form.name.data)
        user.set_username(update_user_form.username.data)
        user.set_password(update_user_form.password.data)
        user.set_email(update_user_form.email.data)
        user.set_gender(update_user_form.gender.data)
        user.set_security_question(update_user_form.security_question.data)
        user.set_security_answer(update_user_form.security_answer.data)
        user.set_account_status(update_user_form.account_status.data)
        user.set_account_type(update_user_form.account_type.data)

        db['Users'] = users_dict
        db.close()

        return redirect(url_for('retrieve_users'))
    else:
        users_dict = {}
        db = shelve.open('user.db', 'r')
        users_dict = db['Users']
        db.close()

        user = users_dict.get(id)
        update_user_form.name.data = user.get_name()
        update_user_form.username.data = user.get_username()
        update_user_form.password.data = user.get_password()
        update_user_form.email.data = user.get_email()
        update_user_form.gender.data = user.get_gender()
        update_user_form.security_question.data = user.get_security_question()
        update_user_form.security_answer.data = user.get_security_answer()
        update_user_form.account_status.data = user.get_account_status()
        update_user_form.account_type.data = user.get_account_type()

        return render_template('update_account.html', form=update_user_form)

@app.route('/deleteUser/<int:id>', methods=['POST'])
def delete_user(id):
    users_dict = {}
    db = shelve.open('user.db', 'w')
    users_dict = db['Users']

    users_dict.pop(id)

    db['Users'] = users_dict
    db.close()

    return redirect(url_for('retrieve_users'))

@app.route("/reset", methods=['GET', 'POST'])
def reset():
    reset_user_form = ResetUserForm(request.form)
    error_reset = 0
    if request.method == 'POST' and reset_user_form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'r')
        users_dict = db['Users']
        db.close()
        for key in users_dict:
            if reset_user_form.username.data == users_dict[key].get_username():
                email = users_dict[key].get_email()
                if reset_user_form.email.data == email:
                    return redirect(url_for('security', id=users_dict[key].get_user_id()))

                else:
                    error_reset = error_reset + 1

            else:
                error_reset = error_reset + 1
    if error_reset > 0:
        flash("Invalid Username or Email","default")



    return render_template('reset.html', form=reset_user_form, title = "Reset Page")

@app.route('/security/<int:id>', methods=['GET', 'POST'])
def security(id):
    users_dict = {}
    db = shelve.open('user.db', 'r')
    users_dict = db['Users']
    db.close()
    error_security = 0
    question = users_dict[id].get_security_question()
    security_user_form = SecurityForm(request.form)
    if request.method == 'POST' and security_user_form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'r')
        users_dict = db['Users']
        db.close()

        if security_user_form.security_answer.data == users_dict[id].get_security_answer():
            return redirect(url_for('changepassword', id=users_dict[id].get_user_id()))

        else:
            error_security = error_security + 1
    if error_security > 0:
        flash("Wrong Answer","default")


    return render_template('security.html',question = question, id = id, form=security_user_form, title = "Security Page")

@app.route("/changepassword/<int:id>", methods=["GET","POST"])
def changepassword(id):
    change_password_form = ChangePasswordForm(request.form)
    if request.method == 'POST' and change_password_form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'w')
        users_dict = db['Users']

        user = users_dict.get(id)
        user.set_password(change_password_form.password.data)

        db['Users'] = users_dict
        db.close()

        return redirect(url_for('login'))
    else:
        users_dict = {}
        db = shelve.open('user.db', 'r')
        users_dict = db['Users']
        db.close()

        user = users_dict.get(id)
        change_password_form.password.data = user.get_password()


    return render_template('change_password.html', id=id, form = change_password_form, title="Change Password Page")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = CreateUserForm(request.form)
    users_dict = {}
    db = shelve.open('user.db', 'r')
    users_dict = db['Users']
    db.close()
    repeat = 0
    for key in users_dict:
        if signup_form.username.data == users_dict[key].get_username():
            repeat = 1
            flash("Username is taken", "username")
            break
    for key in users_dict:
        if signup_form.email.data == users_dict[key].get_email():
            repeat = 1
            flash("Email is taken", "email")
            break
    if request.method == 'POST' and signup_form.validate() and repeat == 0:
        users_dict = {}
        db = shelve.open('user.db', 'c')

        try:
            users_dict = db['Users']
        except:
            print("Error in retrieving Users from user.db.")

        user = Account_Class.User(signup_form.name.data, signup_form.username.data, signup_form.password.data, signup_form.email.data, signup_form.gender.data, signup_form.security_question.data, signup_form.security_answer.data, signup_form.account_status.data, signup_form.account_type.data)
        users_dict[user.get_user_id()] = user
        db['Users'] = users_dict

        db.close()

        return redirect(url_for('login'))
    return render_template('signup.html', form=signup_form)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    settings_form = UpdateUserForm(request.form)
    users_dict = {}
    db = shelve.open('user.db', 'r')
    users_dict = db['Users']
    db.close()
    repeat = 0
    id = session["customer_id"]
    username = users_dict[id].get_username()
    email = users_dict[id].get_email()
    for key in users_dict:
        if settings_form.username.data == users_dict[key].get_username():
            if settings_form.username.data == username:
                repeat = repeat + 0
            else:
                repeat = repeat + 1
                flash("Username is taken (Revert back to original)", "username")
            break
    for key in users_dict:
        if settings_form.email.data == users_dict[key].get_email():
            if settings_form.email.data == email:
                repeat = repeat + 0
            else:
                repeat = repeat + 1
                flash("Email is taken (Revert back to original)", "email")
                break
    if request.method == 'POST' and settings_form.validate() and repeat < 1:
        users_dict = {}
        db = shelve.open('user.db', 'w')
        users_dict = db['Users']

        user = users_dict.get(id)
        user.set_name(settings_form.name.data)
        user.set_username(settings_form.username.data)
        user.set_password(settings_form.password.data)
        user.set_email(settings_form.email.data)
        user.set_gender(settings_form.gender.data)
        user.set_security_question(settings_form.security_question.data)
        user.set_security_answer(settings_form.security_answer.data)
        user.set_account_status(settings_form.account_status.data)
        user.set_account_type(settings_form.account_type.data)

        db['Users'] = users_dict
        db.close()

        return redirect(url_for('cust_homepage', id=users_dict[id].get_user_id()))
    else:
        users_dict = {}
        db = shelve.open('user.db', 'r')
        users_dict = db['Users']
        db.close()

        user = users_dict.get(id)
        settings_form.name.data = user.get_name()
        settings_form.username.data = user.get_username()
        settings_form.password.data = user.get_password()
        settings_form.email.data = user.get_email()
        settings_form.gender.data = user.get_gender()
        settings_form.security_question.data = user.get_security_question()
        settings_form.security_answer.data = user.get_security_answer()
        settings_form.account_status.data = user.get_account_status()
        settings_form.account_type.data = user.get_account_type()

        return render_template('settings.html', id=id, form=settings_form)

@app.route('/logout')
def logout():
    session.pop("customer_id")
    session.pop("customer_email")
    session.pop("customer_username")
    return redirect(url_for('home'))
#
#Terron routing
#
@app.route('/createFeedback', methods=['GET', 'POST'])
def create_feedback():
    create_feedback_form = CreateFeedbackForm(request.form)
    if request.method == 'POST' and create_feedback_form.validate():
        feedbacks_dict = {}
        db = shelve.open('feedback.db', 'c')

        try:
            feedbacks_dict = db['Feedbacks']
        except:
            print("Error in retrieving Feedbacks from feedback.db.")

        feedback = Feedback.Feedback(create_feedback_form.membership.data, create_feedback_form.remarks.data)
        feedbacks_dict[feedback.get_feedback_id()] = feedback
        db['Feedbacks'] = feedbacks_dict

        db.close()

        return redirect(url_for('thank_you'))
    return render_template('createFeedback.html', form=create_feedback_form)

@app.route('/viewFeedback')
def view_feedback():
    feedbacks_dict = {}
    db = shelve.open('feedback.db', 'r')
    feedbacks_dict = db['Feedbacks']
    db.close()

    feedbacks_list = []
    for key in feedbacks_dict:
        feedback = feedbacks_dict.get(key)
        feedbacks_list.append(feedback)
    return render_template('view_feedback.html', count=len(feedbacks_list), feedbacks_list=feedbacks_list)

@app.route('/thankyou')
def thank_you():

    return render_template('thankyou.html')

@app.route('/retrieveFeedbacks')
def retrieve_feedbacks():
    feedbacks_dict = {}
    db = shelve.open('feedback.db', 'r')
    feedbacks_dict = db['Feedbacks']
    db.close()

    feedbacks_list = []
    for key in feedbacks_dict:
        feedback = feedbacks_dict.get(key)
        feedbacks_list.append(feedback)

    return render_template('retrieveFeedbacks.html', count=len(feedbacks_list), feedbacks_list=feedbacks_list)


@app.route('/updateFeedback/<int:id>', methods=['GET', 'POST'])
def update_feedback(id):
    update_feedback_form = CreateFeedbackForm(request.form)
    if request.method == 'POST' and update_feedback_form.validate():
        feedbacks_dict = {}
        db = shelve.open('feedback.db', 'w')
        feedbacks_dict = db['Feedbacks']

        feedback = feedbacks_dict.get(id)

        feedback.set_membership(update_feedback_form.membership.data)
        feedback.set_remarks(update_feedback_form.remarks.data)

        db['Feedbacks'] = feedbacks_dict
        db.close()

        return redirect(url_for('retrieve_feedbacks'))
    else:
        feedbacks_dict = {}
        db = shelve.open('feedback.db', 'r')
        feedbacks_dict = db['Feedbacks']
        db.close()

        feedback = feedbacks_dict.get(id)

        update_feedback_form.membership.data = feedback.get_membership()
        update_feedback_form.remarks.data = feedback.get_remarks()

        return render_template('updateFeedback.html', form=update_feedback_form)




@app.route('/deleteFeedback/<int:id>', methods=['POST'])
def delete_feedback(id):
    feedbacks_dict = {}
    db = shelve.open('feedback.db', 'w')
    feedbacks_dict = db['Feedbacks']

    feedbacks_dict.pop(id)

    db['Feedbacks'] = feedbacks_dict
    db.close()

    return redirect(url_for('retrieve_feedbacks'))

@app.route('/deleteFeedbackCustomer/<int:id>', methods=['POST'])
def delete_feedbackCustomer(id):
    feedbacks_dict = {}
    db = shelve.open('feedback.db', 'w')
    feedbacks_dict = db['Feedbacks']

    feedbacks_dict.pop(id)

    db['Feedbacks'] = feedbacks_dict
    db.close()

    return redirect(url_for('view_feedback'))

#
#yuriel routing
#
@app.route('/createBlog', methods=['GET', 'POST'])
def create_blog():
    create_blog_form = CreateBlogForm(request.form)
    if request.method == 'POST' and create_blog_form.validate():

        blogs_dict = {}
        db = shelve.open('report_and_blog.db', 'c')
        try:
            blogs_dict = db['Blogs']
        except:
            print("Error in retrieving Blog from report_and_blog.db.")

        img = request.files.getlist('image')[0]
        filepath = generate_image_id(img)
        if filepath:
            img.save(filepath)
        else:
            if filepath is None:
                pass
            else:
                alert = 'true'
                return redirect(url_for('create_blog', alert=alert))

        blog_id = str(generate_blog_id())
        account = session['customer_id']
        username = session['customer_username']
        blog = Blog(blog_id=blog_id, account=account, blog_subject=create_blog_form.post_name.data,
                    image=filepath, blog_content=create_blog_form.post_content.data,
                    category=create_blog_form.category.data, upvote_count=0, account_username=username)
        blogs_dict[blog.get_blog_id()] = blog
        db['Blogs'] = blogs_dict

        # Test codes
        blogs_dict = db['Blogs']
        blog = blogs_dict[blog.get_blog_id()]
        print("Blog with ID", blog.get_blog_id(), "was stored in report_and_blog.db successfully")
        db.close()
        flash(f"Blog {blog.get_blog_id()} is successfully created.")
        return redirect(url_for('search_blog', search_query='all'))
    return render_template('createBlog.html', form=create_blog_form)


@app.route('/searchBlog/<search_query>', methods=['GET', 'POST'])
def search_blog(search_query):
    search_blog_form = SearchBlogForm(request.form)
    create_comment_form = CreateCommentForm(request.form)
    blogs_dict = {}
    blogs_temp_dict = {}
    db = shelve.open('report_and_blog.db', 'c')
    try:
        blogs_dict = db['Blogs']
        blogs_temp_dict = db['Temp_Blogs']
    except:
        print("Error in retrieving Blog or Blog_Temp_Dict from report_and_blog.db.")

    if request.method == 'POST' and search_blog_form.validate():

        searched_post_name = search_blog_form.post_name.data.strip()
        searched_post_name_length = len(searched_post_name)
        search_query = searched_post_name # updates search_query
        if search_query == '':
            search_query = 'all'
        blogs_list = []

        if searched_post_name is None:  # checks if user wants to see all blogs
            for key in blogs_dict:
                blog = blogs_dict.get(key)
                blogs_list.append(blog)
        else:
            for key in blogs_dict:
                blog = blogs_dict.get(key)
                blog_post_name = blog.get_post_name()
                if searched_post_name[0:searched_post_name_length].lower() in blog_post_name.lower(): # lower all characters and check
                    blogs_list.append(blog)

        # saves into temporary database
        blogs_temp_dict['temp_list'] = blogs_list
        db['Temp_Blogs'] = blogs_temp_dict
        db.close()

        return redirect(url_for('search_blog', search_query=search_query))
    else:
        blogs_temp_dict = db['Temp_Blogs']
        blogs_list = blogs_temp_dict['temp_list']  # if KeyError, appears, add blogs_temp_dict['temp_list'] = [] above this line to give the key the value

        # updates comments in temp_db
        for key in blogs_dict:
            perm_blog = blogs_dict.get(key)
            for temp_blog in blogs_list:
                if temp_blog.get_blog_id() == perm_blog.get_blog_id():
                    temp_blog.set_comments(perm_blog.get_comments())
                    break

        db.close()

        # paginate
        paginated_info = paginate(request.args.get('page', 1, type=int), blogs_list, blogs_temp_dict['temp_list'],
        'search_Blogs')
        return render_template('searchBlog.html',
        form=search_blog_form, blogs_per_page=paginated_info[0], total_pages=paginated_info[1],
        page=paginated_info[2], comment_form=create_comment_form, search_query=search_query)


@app.route("/add_comment/<search_query>", methods=["POST"])
def add_comment(search_query):
    create_comment_form = CreateCommentForm(request.form)
    blogs_dict = {}
    comments_dict = {}
    temp_blogs_dict = {}
    db = shelve.open('report_and_blog.db', 'c')
    try:
        blogs_dict = db['Blogs']
        temp_blogs_dict = db['Temp_Blogs']
    except:
        print("Error in retrieving Comments from report_and_blog.db.")

    if request.method == 'POST' and create_comment_form.validate():
        comment_content = create_comment_form.comment_content.data
        print(comment_content)
        if comment_content.strip() == '':  # checks if user enters comment or not; WIP can edit to do front-end validation
            # with JS instead
            return redirect(url_for('search_blog', search_query=search_query))
        comment_blog_id = request.form.get("blog_id")

        # update all comment lists in blogs_dict
        for key in blogs_dict:
            blog = blogs_dict.get(key)
            if blog.get_blog_id() == comment_blog_id:
                # create comment object
                original_datetime = datetime.datetime.now()
                formatted_datetime = original_datetime.strftime("%Y-%m-%d %H:%M:%S")
                comment_id = str(generate_comment_id())
                account = session['customer_username']
                comment = Comment(comment_id=comment_id, blog_id=comment_blog_id, comment_content=comment_content, created_by=account,
                                  date_created=formatted_datetime)

                # add comment object to database
                comments = blog.get_comments()
                comments.append(comment)
                blog.set_comments(comments)
                comments_dict[comment.get_blog_id()] = comments

        # finalises database
        db['Blogs'] = blogs_dict
        db['Temp_Blogs'] = temp_blogs_dict
        db.close()
        flash("Comment successfully created.")
        return redirect(url_for('search_blog', search_query=search_query))


@app.route('/allBlogs')
def retrieve_blogs():
    blogs_dict = {}
    db = shelve.open('report_and_blog.db', 'r')
    blogs_dict = db['Blogs']
    db.close()

    blogs_list = []
    for key in blogs_dict:
        blog = blogs_dict.get(key)
        blogs_list.append(blog)
    paginated_info = paginate(request.args.get('page', 1, type=int), blogs_list, len(blogs_list), 'all_Blogs')
    return render_template('allBlogs.html', count=len(blogs_list), blogs_list=blogs_list,
    blogs_per_page=paginated_info[0], total_pages=paginated_info[1], page=paginated_info[2])


@app.route('/allComments/<blog_id>')
# @login_required
def retrieve_comments(blog_id):
    blogs_dict = {}
    db = shelve.open('report_and_blog.db', 'r')
    blogs_dict = db['Blogs']
    db.close()

    comments_list = []
    for key in blogs_dict:
        blog = blogs_dict.get(key)
        if blog.get_blog_id() == blog_id:
            for comment in blog.get_comments():
                comments_list.append(comment)

    paginated_info = paginate(request.args.get('page', 1, type=int), comments_list, len(comments_list), 'all_Comments')

    return render_template('allComments.html', count=len(comments_list), comments_list=comments_list,
    comments_per_page=paginated_info[0], total_pages=paginated_info[1], page=paginated_info[2])


@app.route('/deleteComment/<blog_id>/<comment_id>', methods=['POST'])
def delete_comment(blog_id, comment_id):
    comments_dict = {}
    db = shelve.open('report_and_blog.db', 'w')
    blogs_dict = db['Blogs']

    for key in blogs_dict:
        blog = blogs_dict.get(key)
        if blog.get_blog_id() == blog_id:
            for comment in blog.get_comments():
                if comment_id == comment.get_comment_id():
                    blog.get_comments().remove(comment)
                    blog.set_comments(blog.get_comments())

    db['Blogs'] = blogs_dict
    db.close()

    return redirect(url_for('retrieve_comments', blog_id=blog_id))


@app.route('/updateBlog/<int:id>/', methods=['GET', 'POST'])
def update_blog(id):
    update_blog_form = CreateBlogForm(request.form)
    if request.method == 'POST' and update_blog_form.validate():
        blogs_dict = {}
        db = shelve.open('report_and_blog.db', 'w')
        blogs_dict = db['Blogs']

        blog = blogs_dict.get(str(id))

        # remove old image from static/files and change to new picture

        img = request.files.getlist('image')[0]
        new_filepath = generate_image_id(img)
        old_filepath = blog.get_image()

        if new_filepath is not None:
            if new_filepath:
                img.save(new_filepath)  # save new filepath from static/files if not None
            else:
                alert = 'true'
                return redirect(url_for('update_blog', id=id, alert=alert))
        if old_filepath is not None:
            os.remove(old_filepath)  # remove old filepath from static/files if not None

        blog.set_post_name(update_blog_form.post_name.data)
        blog.set_image(new_filepath)
        blog.set_post_content(update_blog_form.post_content.data)
        blog.set_category(update_blog_form.category.data)

        db['Blogs'] = blogs_dict
        db.close()

        return redirect(url_for('retrieve_blogs'))
    else:
        blogs_dict = {}
        db = shelve.open('report_and_blog.db', 'r')
        blogs_dict = db['Blogs']
        db.close()

        blog = blogs_dict.get(str(id))
        update_blog_form.post_name.data = blog.get_post_name()
        update_blog_form.image.data = blog.get_image()
        update_blog_form.post_content.data = blog.get_post_content()
        update_blog_form.category.data = blog.get_category()

        return render_template('updateBlog.html', form=update_blog_form)


@app.route('/deleteBlog/<id>', methods=['POST'])
def delete_blog(id):
    blogs_dict = {}
    db = shelve.open('report_and_blog.db', 'w')
    blogs_dict = db['Blogs']

    blog_to_be_deleted = blogs_dict[str(id)]
    image_path = blog_to_be_deleted.get_image()
    if image_path is not None:
        os.remove(image_path)

    blogs_dict.pop(str(id))
    db['Blogs'] = blogs_dict
    db.close()
    flash(f"Blog {blog_to_be_deleted.get_blog_id()} is successfully deleted.")
    return redirect(url_for('retrieve_blogs'))


@app.route('/reportedSubmitted', methods=['GET'])
def report_confirmed():
    return render_template('reportSubmitted.html')


@app.route('/reportBlog/<blog_id>', methods=['GET', 'POST'])
def submit_report(blog_id):
    if blog_id == 'blog':
        blog_id = ''
    create_report_form = CreateReportForm(request.form, reported_account=blog_id)
    if request.method == 'POST' and create_report_form.validate():
        reports_dict = {}
        db = shelve.open('report_and_blog.db', 'c')
        try:
            reports_dict = db['Reports']
            blogs_dict = db['Blogs']
        except:
            print("Error in retrieving Blog from report_and_blog.db.")

        if check_report_id(create_report_form.reported_account.data) is False:
            blog_id = 'blog'
            alert = 'true'
            return redirect(url_for('submit_report', alert=alert, blog_id=blog_id))

        account = session['customer_id']
        email = session['customer_email']
        report = Report(account=account, reporter_email=email, reported_blog_id=create_report_form.reported_account.data,
                        reported_subjects=create_report_form.report_subjects.data,
                        report_reason=create_report_form.report_reason.data)
        report.set_report_id(generate_report_id())
        reports_dict[report.get_report_id()] = report
        db['Reports'] = reports_dict

        # Test codes
        reports_dict = db['Reports']
        report = reports_dict[report.get_report_id()]
        print(report.get_report_id(), "was stored in report_and_blog.db successfully")
        db.close()

        return redirect(url_for('cust_homepage'))
    return render_template('reportBlog.html', form=create_report_form)


@app.route('/unresolvedReports')
def retrieve_reports():
    reports_dict = {}
    db = shelve.open('report_and_blog.db', 'r')
    reports_dict = db['Reports']
    db.close()

    reports_list = []
    for key in reports_dict:
        report = reports_dict.get(key)
        reports_list.append(report)

    return render_template('unresolvedReports.html', count=len(reports_list), reports_list=reports_list)


@app.route('/sendReportEmail/<report_id>/<verdict>', methods=['GET', 'POST'])
def send_report_email(report_id, verdict):
    reports_dict = {}
    db = shelve.open('report_and_blog.db', 'c')
    reports_dict = db['Reports']

    for key in reports_dict:
        report = reports_dict.get(key)
        if str(report.get_report_id()) == str(report_id):
            send_report_confirmation_email(report.get_reporter_email(), report.get_account(), verdict)
            reports_dict.pop(report.get_report_id())
            break

    db['Reports'] = reports_dict
    db.close()
    return redirect(url_for('retrieve_reports'))


@app.route('/generate_pdf')
def generate_pdf():
    try:
        blog_db = shelve.open('report_and_blog.db', 'r')
        product_db = shelve.open('product.db', 'r')
        account_db = shelve.open('user.db', 'r')
        payment_db = shelve.open('payment.db', 'r')
        feedback_db = shelve.open('feedback.db', 'r')
    except:
        print('Error in opening DBs')
    else:
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        generated_by = session['customer_id']
        pdf_creator = PDFExporter(date, generated_by)
        pdf_creator.add_blog_data_page(blog_db)
        pdf_creator.add_product_data_page(product_db)
        pdf_creator.add_account_data_page(account_db)
        pdf_creator.add_payment_data_page(payment_db)
        pdf_creator.add_feedback_data_page(feedback_db)
        generate_pdf_id = pdf_creator.export_pdf()

        return redirect(f'static/reports/{generate_pdf_id}GU_progress_report.pdf')


if __name__ == "__main__":
    app.run(debug=True, port=5000)
