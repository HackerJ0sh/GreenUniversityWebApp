# User class
class User:
    count_id = 0

    # initializer method
    def __init__(self, product_name, last_name, gender, remarks, quantity):
        User.count_id += 1
        self.__user_id = User.count_id
        self.__product_name = product_name
        self.__last_name = last_name
        self.__gender = gender
      
        self.__remarks = remarks
        self.__quantity = quantity
        

    # accessor methods
    def get_user_id(self):
        return self.__user_id
    
    def get_product_name(self):
        return self.__product_name

    def get_last_name(self):
        return self.__last_name

    def get_gender(self):
        return self.__gender

    

    def get_remarks(self):
        return self.__remarks
    
    def get_quantity(self):
        return self.__quantity

    # mutator methods
    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_product_name(self, product_name):
        self.__product_name = product_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_gender(self, gender):
        self.__gender = gender

   

    def set_remarks(self, remarks):
        self.__remarks = remarks

    def set_quantity(self, quantity):
        self.__quantity = quantity
