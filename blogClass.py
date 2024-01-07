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

