from flask import Flask, render_template, request, redirect, url_for
from Forms import CreateUserForm
from flask_wtf.file import FileAllowed
import shelve, User , Cart, random

app = Flask(__name__)


@app.route('/')
def home():
    users_dict = {}
    db = shelve.open('user.db', 'r')
    users_dict = db['Users']
    db.close()
    
    
    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)
        
        

    return render_template('home.html', count=len(users_list), users_list=users_list)

@app.route('/<int:id>/info', methods=["POST", "GET"])
def info(id):
    users_dict = {}
    db = shelve.open('user.db', 'r')
    users_dict = db['Users']
    db.close()

    users_list = []
    
    user = users_dict.get(id)
    users_list.append(user)
    
    return render_template('info.html', users_list=users_list)

@app.route('/cart')
def cart():
    cart_dict = {}
    db = shelve.open('cart.db','r')
    cart_dict = db['Users']
    db.close()

    cart_list = []
    total_price = 0
    for key in cart_dict:
        user = cart_dict.get(key)
        cart_list.append(user)
        price = user.get_last_name()
        total_price += float(price)
    
    total_price = f"{total_price:.2f}"
    return render_template('cart.html', cartcount=len(cart_list), cart_list=cart_list,total=total_price)

@app.route('/<int:id>/add_to_cart', methods=["POST", "GET"])
def add_to_cart(id):
    users_dict = {}
    db = shelve.open('user.db', 'r')
    users_dict = db['Users']
    user = users_dict.get(id)
    db.close()

    cart_dict = {}
    db2 = shelve.open('cart.db','w')
    cart_dict = db2['Users']
    cart_dict[id] = user
    db2['Users'] = cart_dict
    db.close()
    
    return redirect(url_for('cart'))

        
@app.route('/<int:id>/remove_from_cart', methods=['POST'])
def remove_from_cart(id):
    users_dict = {}
    db = shelve.open('cart.db', 'w')
    users_dict = db['Users']

    users_dict.pop(id)

    db['Users'] = users_dict
    db.close()

    return redirect(url_for('cart'))
        

         
    



@app.route('/contactUs')
def contact_us():
    return render_template('contactUs.html')

@app.route('/invalidfile')
def invalid_file():
    return render_template('invalidfile.html')



@app.route('/createUser', methods=['GET', 'POST'])
def create_user():
    create_user_form = CreateUserForm(request.form)
    allowed_extensions_list = ['jpg','png']  
    if request.method == 'POST' and create_user_form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'c')

        try:
            users_dict = db['Users']
        except:
            print("Error in retrieving Users from user.db.")

        
        img = request.files.getlist('image')[0]
        if img.filename.split(".")[-1].lower() not in allowed_extensions_list:
            return redirect(url_for('invalid_file'))
        else:
            user = User.User(create_user_form.first_name.data, 
                         create_user_form.last_name.data, 
                         create_user_form.gender.data, 
                         
                         create_user_form.remarks.data, 
                         create_user_form.quantity.data)
            users_dict[user.get_user_id()] = user
            db['Users'] = users_dict

            db.close()
            img.save(f'./static/images/{user.get_first_name()}.{img.filename.split(".")[-1]}')
            
        # assign a file name to the saved image
        

        return redirect(url_for('retrieve_users'))
    return render_template('createUser.html', form=create_user_form)

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
        
    return render_template('retrieveUsers.html', count=len(users_list), users_list=users_list,)


@app.route('/updateUser/<int:id>/', methods=['GET', 'POST'])
def update_user(id):
    update_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and update_user_form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'w')
        users_dict = db['Users']

        user = users_dict.get(id)
        user.set_first_name(update_user_form.first_name.data)
        user.set_last_name(update_user_form.last_name.data)
        user.set_gender(update_user_form.gender.data)
        
        user.set_remarks(update_user_form.remarks.data)
        user.set_quantity(update_user_form.quantity.data)

        db['Users'] = users_dict
        db.close()
        

        return redirect(url_for('retrieve_users'))
    else:
        users_dict = {}
        db = shelve.open('user.db', 'r')
        users_dict = db['Users']
        db.close()

        user = users_dict.get(id)
        update_user_form.first_name.data = user.get_first_name()
        update_user_form.last_name.data = user.get_last_name()
        update_user_form.gender.data = user.get_gender()
        
        update_user_form.remarks.data = user.get_remarks()
        update_user_form.quantity.data = user.get_quantity()

        return render_template('updateUser.html', form=update_user_form)


@app.route('/deleteUser/<int:id>', methods=['POST'])
def delete_user(id):
    users_dict = {}
    db = shelve.open('user.db', 'w')
    users_dict = db['Users']

    users_dict.pop(id)

    db['Users'] = users_dict
    db.close()

    return redirect(url_for('retrieve_users'))



if __name__ == '__main__':
    app.run()



