from flask import Flask, render_template, request, redirect, url_for, flash
from Account_Forms import CreateUserForm,LoginForm, UpdateUserForm, ResetUserForm, SecurityForm, ChangePasswordForm
import shelve, Account_Class


app = Flask(__name__)
app.secret_key = "Kendrick"

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/cust_home/<int:id>/", methods=['GET', 'POST'])
def cust_homepage(id):
    users_dict = {}
    db = shelve.open('user.db', 'r')
    users_dict = db['Users']
    db.close()
    name = users_dict[id].get_name()
    return render_template("customer_homepage.html", name=name, id = id)

@app.route("/staff_home/<int:id>/", methods=['GET', 'POST'])
def staff_homepage(id):
    users_dict = {}
    db = shelve.open('user.db', 'r')
    users_dict = db['Users']
    db.close()
    name = users_dict[id].get_name()
    return render_template("staff_homepage.html", name=name, id = id)

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
                                  register_user_form.security_answer.data)
        users_dict[user.get_user_id()] = user
        db['Users'] = users_dict

        db.close()

        return redirect(url_for('retrieve_users'))
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
        for key in users_dict:
            if login_user_form.username.data == users_dict[key].get_username():
                password = users_dict[key].get_password()
                if login_user_form.password.data == password:
                    if users_dict[key].get_account_type() == "S":
                        return redirect(url_for('staff_homepage', id=users_dict[key].get_user_id()))
                    else:
                        return redirect(url_for('cust_homepage', id=users_dict[key].get_user_id()))
                else:
                    error_login = error_login + 1

            else:
                error_login = error_login + 1
        if error_login > 0:
            flash("Wrong Username or Password")


    return render_template('login2.html', form=login_user_form, title = "Login Page")

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
    return render_template('create_account.html', form=create_user_form)

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
        flash("Invalid Username or Email")



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
        flash("Wrong Answer")


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

@app.route('/settings/<int:id>/', methods=['GET', 'POST'])
def settings(id):
    settings_form = UpdateUserForm(request.form)
    users_dict = {}
    db = shelve.open('user.db', 'r')
    users_dict = db['Users']
    db.close()
    repeat = 0
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

        return render_template('settings.html', form=settings_form)

if __name__ == '__main__':
    app.run()

