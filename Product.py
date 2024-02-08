# Product class
class Product:
    count_id = 0

    # initializer method
    def __init__(self, product_name, product_price, product_category, remarks, quantity):
        Product.count_id += 1
        self.__product_id = Product.count_id
        self.__product_name = product_name
        self.__product_price = product_price
        self.__product_category = product_category
      
        self.__remarks = remarks
        self.__quantity = quantity
        

    # accessor methods
    def get_product_id(self):
        return self.__product_id
    
    def get_product_name(self):
        return self.__product_name

    def get_product_price(self):
        return self.__product_price

    def get_product_category(self):
        return self.__product_category

    

    def get_remarks(self):
        return self.__remarks
    
    def get_quantity(self):
        return self.__quantity

    # mutator methods
    def set_product_id(self, product_id):
        self.__product_id = product_id

    def set_product_name(self, product_name):
        self.__product_name = product_name

    def set_product_price(self, product_price):
        self.__product_price = product_price

    def set_product_category(self, product_category):
        self.__product_category = product_category

   

    def set_remarks(self, remarks):
        self.__remarks = remarks

    def set_quantity(self, quantity):
        self.__quantity = quantity
