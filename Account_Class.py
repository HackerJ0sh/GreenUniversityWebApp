# User class
class User():
    count_id = 0

    # initializer method
    def __init__(self, name, username, password, email, gender, security_question, security_answer, account_status, account_type):
        User.count_id += 1
        self.__user_id = User.count_id
        self.__name = name
        self.__username = username
        self.__password = password
        self.__email = email
        self.__gender = gender
        self.__security_question = security_question
        self.__security_answer = security_answer
        self.__account_status = account_status
        self.__account_type = account_type

    # accessor methods
    def get_user_id(self):
        return self.__user_id

    def get_name(self):
        return self.__name

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def get_email(self):
        return self.__email

    def get_gender(self):
        return self.__gender

    def get_security_question(self):
        return self.__security_question

    def get_security_answer(self):
        return self.__security_answer

    def get_account_status(self):
        return self.__account_status

    def get_account_type(self):
        return self.__account_type

    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_name(self, name):
        self.__name = name

    def set_username(self, username):
        self.__username = username

    def set_password(self, password):
        self.__password = password

    def set_email(self, email):
        self.__email = email

    def set_gender(self, gender):
        self.__gender = gender

    def set_security_question(self, security_question):
        self.__security_question = security_question

    def set_security_answer(self, security_answer):
        self.__security_answer = security_answer

    def set_account_status(self, account_status):
        self.__account_status = account_status

    def set_account_type(self, account_type):
        self.__account_type = account_type