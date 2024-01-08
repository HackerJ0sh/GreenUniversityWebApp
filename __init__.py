from flask import Flask, render_template, request, redirect, url_for
from blogForm import CreateBlogForm
import shelve
import blogClass


app = Flask(__name__, template_folder='customerTemplates')


@app.route('/')
def homepage():
    return render_template('customerHomepage.html')


@app.route('/createBlog', methods=['GET', 'POST'])
def create_blog():
    create_blog_form = CreateBlogForm(request.form)
    if request.method == 'POST' and create_blog_form.validate():

        blogs_dict = {}
        db = shelve.open('blogs.db', 'c')
        try:
            blogs_dict = db['Blogs']
        except:
            print("Error in retrieving Blog from blogs.db.")

        blog = blogClass.Blog(account=None, blog_subject=create_blog_form.post_name.data,
            image=create_blog_form.image.data, blog_content=create_blog_form.post_content.data,
            category=create_blog_form.category.data, upvote_count=0)
        blogs_dict[blog.get_blog_id()] = blog
        db['Blogs'] = blogs_dict

        # Test codes
        blogs_dict = db['Blogs']
        blog = blogs_dict[blog.get_blog_id()]
        print(blog.get_blog_id(), "was stored in blogs.db successfully")
        db.close()

        return redirect(url_for('homepage'))
    return render_template('createBlog.html', form=create_blog_form)


@app.route('/allBlogs')
def retrieve_blogs():
    blogs_dict = {}
    db = shelve.open('blogs.db', 'r')
    blogs_dict = db['Blogs']
    db.close()

    blogs_list = []
    for key in blogs_dict:
        blog = blogs_dict.get(key)
        blogs_list.append(blog)

    return render_template('allBlogs.html', count=len(blogs_list), blogs_list=blogs_list)

@app.route('/updateBlog/<int:id>/', methods=['GET', 'POST'])
def update_blog(id):
    update_blog_form = CreateBlogForm(request.form)
    if request.method == 'POST' and update_blog_form.validate():
        blogs_dict = {}
        db = shelve.open('blogs.db', 'w')
        blogs_dict = db['Blogs']

        blog = blogs_dict.get(id)
        blog.set_post_name(update_blog_form.post_name.data)
        blog.set_image(update_blog_form.image.data)
        blog.set_post_content(update_blog_form.post_content.data)
        blog.set_category(update_blog_form.category.data)

        db['Blogs'] = blogs_dict
        db.close()

        return redirect(url_for('retrieve_blogs'))
    else:
        blogs_dict = {}
        db = shelve.open('blogs.db', 'r')
        blogs_dict = db['Blogs']
        db.close()

        blog = blogs_dict.get(id)
        update_blog_form.post_name.data = blog.get_post_name()
        update_blog_form.image.data = blog.get_image()
        update_blog_form.post_content.data = blog.get_post_content()
        update_blog_form.category.data = blog.get_category()

        return render_template('updateBlog.html', form=update_blog_form)


@app.route('/deleteBlog/<int:id>', methods=['POST'])
def delete_blog(id):
    blogs_dict = {}
    db = shelve.open('blogs.db', 'w')
    blogs_dict = db['Blogs']
    blogs_dict.pop(id)
    db['Blogs'] = blogs_dict
    db.close()

    return redirect(url_for('retrieve_blogs'))




if __name__ == '__main__':
    app.run()


