# base class code
class Blog:
    def __init__(self, blog_id, account, blog_subject, image, blog_content, category, upvote_count, account_username):
        self.__blog_id = blog_id
        self.__account = account
        self.__category = category
        self.__post_name = blog_subject
        self.__image = image
        self.__post_content = blog_content
        self.__upvote_count = upvote_count
        self.__comments = []
        self.__account_username = account_username

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

    def set_category(self, category):
        self.__category = category

    def set_comments(self, comments):
        self.__comments = comments

    def set_account_username(self, account_username):
        self.__account_username = account_username

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

    def get_category(self):
        return self.__category

    def get_comments(self):
        return self.__comments

    def get_account_username(self):
        return self.__account_username



class Comment:
    def __init__(self, blog_id, comment_content, created_by, date_created):
        self.__blog_id = blog_id
        self.__comment_content = comment_content
        self.__created_by = created_by
        self.__date_created = date_created

    def set_blog_id(self, blog_id):
        self.__blog_id = blog_id

    def set_comment_content(self, comment_content):
        self.__comment_content = comment_content

    def set_created_by(self, created_by):
        self.__created_by = created_by

    def set_date_created(self, date_created):
        self.__date_created = date_created

    def get_blog_id(self):
        return self.__blog_id

    def get_comment_content(self):
        return self.__comment_content

    def get_created_by(self):
        return self.__created_by

    def get_date_created(self):
        return self.__date_created


class User:
    count_id = 0

    # initializer method
    def __init__(self):
        User.count_id += 1
        self.__user_id = User.count_id
        self.__name = None
        self.__username = None
        self.__password = None
        self.__email = None
        self.__gender = None
        self.__security_question = None
        self.__security_answer = None
        self.__account_status = None
        self.__account_type = None
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

    def __init__(self, account, reported_blog_id, reported_subjects, report_reason):
        Report.report_id += 1
        self.__account = account
        self.__report_id = Report.report_id
        self.__reported_blog_id = reported_blog_id
        self.__reported_subjects = reported_subjects
        self.__report_reason = report_reason

    def set_report_id(self, report_id):
        self.__report_id = report_id

    def set_reported_blog_id(self, reported_account_id):
        self.__reported_blog_id = reported_account_id

    def set_reported_subjects(self, reported_subjects):
        self.__reported_subjects = reported_subjects

    def set_report_reason(self, report_reason):
        self.__report_reason = report_reason

    def get_report_id(self):
        return self.__report_id

    def get_reported_blog_id(self):
        return self.__reported_blog_id

    def get_reported_subjects(self):
        return self.__reported_subjects

    def get_report_reason(self):
        return self.__report_reason
