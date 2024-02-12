# remember to inherit from user class to get the user ID

class PaymentInfo: 
    transaction_count = 0

    def __init__(self, full_name, phone_number, email, address_line_1, address_line_2, country, postal_code, remember, expiry_date_year, cvv, credit_card_number, credit_card_holder, expiry_date_month, donation): 
        PaymentInfo.transaction_count += 1
        self.__user_id = None # set to the user id who made the transaction
        self.__id = PaymentInfo.transaction_count
        self.__full_name = full_name
        self.__phone_number = phone_number
        self.__email = email
        self.__address_line_1 = address_line_1
        self.__address_line_2 = address_line_2
        self.__postal_code = postal_code
        self.__country = country 
        self.__cvv = cvv
        self.__expiry_date_year = expiry_date_year
        self.__expiry_date_month = expiry_date_month
        self.__credit_card_holder = credit_card_holder
        self.__credit_card_number = credit_card_number
        self.__remember = remember
        self.__donation = donation

    def get_id(self):
        return self.__id
    
    def get_user_id(self):
        return self.__user_id
    
    def get_email(self):
        return self.__email
    
    def get_full_name(self):
        return self.__full_name
    
    def get_phone_number(self):
        return self.__phone_number
    
    def set_email(self, email):
        self.__email = email
    
    def set_full_name(self, full_name):
        self.__full_name = full_name
    
    def set_phone_number(self, phone_number):
        self.__phone_number = phone_number

    def get_address_line_1(self):
        return self.__address_line_1
    
    def get_address_line_2(self):
        return self.__address_line_2
    
    def get_postal_code(self):
        return self.__postal_code
    
    def get_country(self):
        return self.__state
    
    def get_country(self):
        return self.__country
    
    def get_cvv(self):
        return self.__cvv
    
    def get_expiry_date_year(self):
        return self.__expiry_date_year
    
    def get_expiry_date_month(self):
        return self.__expiry_date_month
    
    def get_credit_card_holder(self):
        return self.__credit_card_holder
    
    def get_credit_card_number(self):
        return self.__credit_card_number
    
    def get_remember(self):
        return self.__remember

    def set_address_line_1(self, address_line_1):
        self.__address_line_1 = address_line_1
    
    def set_address_line_2(self, address_line_2):
        self.__address_line_2 = address_line_2

    def get_donation(self):
        return self.__donation
    
    def set_donation(self, donation):
        self.__donation = donation
    
    def set_postal_code(self, postal_code):
        self.__postal_code = postal_code
    
    def set_country(self, country):
        self.__country = country
    
    def set_cvv(self, cvv):
        self.__cvv = cvv
    
    def set_expiry_date_year(self, expiry_date_year):
        self.__expiry_date_year = expiry_date_year
    
    def set_expiry_date_month(self, expiry_date_month):
        self.__expiry_date_month = expiry_date_month
    
    def set_credit_card_holder(self, credit_card_holder):
        self.__credit_card_holder = credit_card_holder
    
    def set_credit_card_number(self, credit_card_number):
        self.__credit_card_number = credit_card_number

    def set_remember(self, remember):
        self.__remember = remember

    def set_user_id(self, id):
        self.__user_id = id 

    def get_user_id(self):
        return self.__user_id