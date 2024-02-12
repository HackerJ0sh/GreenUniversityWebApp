import shelve
import random


def generate_blog_id():
    db = shelve.open('report_and_blog.db', 'c')
    try:
        blogs_dict = db['Blogs']
    except:
        print("Error in retrieving Blog from report_and_blog.db.")

    else:
        blog_id = random.randint(1, 10 ** 15)
        for key in blogs_dict:
            blog = blogs_dict.get(key)
            while blog_id == blog.get_blog_id():
                blog_id = random.randint(1, 10 ** 15)
        return blog_id


def generate_image_id(img):
    allowed_extensions_list = ['jpg', 'png', 'jpeg', '']
    if img.filename.split(".")[-1].lower() not in allowed_extensions_list:
        return False

    if img.filename.split(".")[-1].lower() == '':
        filepath = None
    else:
        filepath = f'./static/files/{random.randint(1, 10 ** 15)}.{img.filename.split(".")[-1].lower()}'
    return filepath


def generate_comment_id():
    db = shelve.open('report_and_blog.db', 'c')
    try:
        blogs_dict = db['Blogs']
    except:
        print("Error in retrieving Blog from report_and_blog.db.")

    else:
        comment_id = random.randint(1, 10 ** 15)
        for key in blogs_dict:
            blog = blogs_dict.get(key)
            comments_list = blog.get_comments()
            while True:
                if comment_id in comments_list:
                    comment_id = random.randint(1, 10 ** 15)
                else:
                    break
        return comment_id


def check_report_id(id):
    reports_dict = {}
    db = shelve.open('report_and_blog.db', 'c')
    try:
        blogs_dict = db['Blogs']
    except:
        print("Error in retrieving Blog from report_and_blog.db.")

    id_found = False
    for key in blogs_dict:
        blog = blogs_dict.get(key)
        if id == blog.get_blog_id():
            id_found = True
    return id_found


def paginate(page, blogs_list, blogs_temp_dict_length, is_for):
    if is_for == 'search_Blogs':
        per_page = 3

        start = (page - 1) * per_page
        end = start + per_page
        total_pages = (len(blogs_temp_dict_length) + per_page - 1) // per_page
        if total_pages == 0:
            total_pages = 1

        blogs_per_page = blogs_list[start:end]
        return blogs_per_page, total_pages, page

    elif is_for == 'all_Blogs':
        per_page = 10

        start = (page - 1) * per_page
        end = start + per_page
        total_pages = (blogs_temp_dict_length + per_page - 1) // per_page
        if total_pages == 0:
            total_pages = 1

        blogs_per_page = blogs_list[start:end]
        return blogs_per_page, total_pages, page

    elif is_for == 'all_Comments':
        per_page = 30

        start = (page - 1) * per_page
        end = start + per_page
        total_pages = (blogs_temp_dict_length + per_page - 1) // per_page
        if total_pages == 0:
            total_pages = 1

        blogs_per_page = blogs_list[start:end]
        return blogs_per_page, total_pages, page

