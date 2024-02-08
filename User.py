# User class
class User:
    count_id = 0

    # initializer method
    def __init__(self, product_name, product_price, product_category, remarks, quantity):
        User.count_id += 1
        self.__user_id = User.count_id
        self.__product_name = product_name
        self.__product_price = product_price
        self.__product_category = product_category
      
        self.__remarks = remarks
        self.__quantity = quantity
        

    # accessor methods
    def get_user_id(self):
        return self.__user_id
    
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
    def set_user_id(self, user_id):
        self.__user_id = user_id

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
