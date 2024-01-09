# base class code
class Blog:
    blog_id = 0

    def __init__(self, account, blog_subject, image, blog_content, category, upvote_count):
        Blog.blog_id += 1
        self.__blog_id = Blog.blog_id
        self.__account = account
        self.__category = category
        self.__post_name = blog_subject
        self.__image = image
        self.__post_content = blog_content
        self.__upvote_count = upvote_count

    def set_blog_id(self, blog_id):
        self.__blog_id = blog_id

    def set_image(self, image):
        self.__image = image

    def set_account(self, account):
        self.__account = account

    def set_post_name(self, post_name):
        self.__post_name = post_name

    def set_post_content(self, post_content):
        self.__post_content = post_content

    def set_upvote_count(self, upvote_count):
        self.__upvote_count = upvote_count

    def set_category(self, category):
        self.__category = category

    def get_blog_id(self):
        return self.__blog_id

    def get_image(self):
        return self.__image

    def get_account(self):
        return self.__account

    def get_post_name(self):
        return self.__post_name

    def get_post_content(self):
        return self.__post_content

    def get_upvote_count(self):
        return self.__upvote_count

    def get_category(self):
        return self.__category


class User:
    count_id = 0

    # initializer method
    def _init_(self, name, username, password, email, gender, security_question, security_answer, account_status, account_type):
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


class Report:
    report_id = 0

    def __init__(self, account, reported_account_id, reported_subjects, report_reason):
        Report.report_id += 1
        self.__account = account
        self.__report_id = Report.report_id
        self.__reported_account_id = reported_account_id
        self.__reported_subjects = reported_subjects
        self.__report_reason = report_reason

    def set_report_id(self, report_id):
        self.__report_id = report_id

    def set_reported_account_id(self, reported_account_id):
        self.__reported_account_id = reported_account_id

    def set_reported_subjects(self, reported_subjects):
        self.__reported_subjects = reported_subjects

    def set_report_reason(self, report_reason):
        self.__report_reason = report_reason

    def get_report_id(self):
        return self.__report_id

    def get_reported_account_id(self):
        return self.__reported_account_id

    def get_reported_subjects(self):
        return self.__reported_subjects

    def get_report_reason(self):
        return self.__report_reason