from flask import Flask, render_template, request, redirect, url_for
from ProductForm import CreateProductForm
from flask_wtf.file import FileAllowed
import shelve, Product , random

app = Flask(__name__)


@app.route('/')
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
    cart_dict = {}
    db = shelve.open('shoppingcart.db','r')
    cart_dict = db['Products']
    db.close()

    cart_list = []
    total_price = 0
    for key in cart_dict:
        product = cart_dict.get(key)
        cart_list.append(product)
        price = product.get_product_price()
        total_price += float(price)
    
    total_price = f"{total_price:.2f}"
    return render_template('cart.html', cartcount=len(cart_list), cart_list=cart_list,total=total_price)

@app.route('/<int:id>/add_to_cart', methods=["POST", "GET"])
def add_to_cart(id):
    products_dict = {}
    db = shelve.open('product.db', 'r')
    products_dict = db['Products']
    product = products_dict.get(id)
    db.close()

    cart_dict = {}
    db2 = shelve.open('shoppingcart.db','w')

    cart_dict = db2['Products']
    cart_dict[id] = product
    db2['Products'] = cart_dict
    db.close()
    
    return redirect(url_for('cart'))

        
@app.route('/<int:id>/remove_from_cart', methods=['POST'])
def remove_from_cart(id):
    products_dict = {}
    db = shelve.open('shoppingcart.db', 'w')
    products_dict = db['Products']

    products_dict.pop(id)

    db['Products'] = products_dict
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



if __name__ == '__main__':
    app.run()



