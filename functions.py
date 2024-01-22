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
        for id in blogs_dict:
            if id == blog_id:
                while blog_id == id:
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


