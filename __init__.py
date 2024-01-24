from flask import Flask, render_template, request, redirect, url_for, session
from functions import *
from blogForm import *
import shelve
from formClasses import *
from reportForm import CreateReportForm
from random import randint
import os

app = Flask(__name__, template_folder='customerTemplates')
app.config['UPLOAD_FOLDER'] = 'static/files'
allowed_extensions_list = ['jpg', 'png', 'jpeg', '']
app.secret_key = 'hwrhwey project'


@app.route('/')
def homepage():
    return render_template('customerHomepage.html')


@app.route('/createBlog', methods=['GET', 'POST'])
def create_blog():
    create_blog_form = CreateBlogForm(request.form)
    if request.method == 'POST' and create_blog_form.validate():

        blogs_dict = {}
        db = shelve.open('report_and_blog.db', 'c')
        try:
            blogs_dict = db['Blogs']
        except:
            print("Error in retrieving Blog from report_and_blog.db.")

        # create test account & generate random id with randint
        random_id = str(randint(1, 1000000))
        test_account = User()
        test_account.set_user_id(random_id)

        img = request.files.getlist('image')[0]
        filepath = generate_image_id(img)
        if filepath:
            img.save(filepath)
        else:
            if filepath is None:
                pass
            else:
                alert = 'true'
                return redirect(url_for('create_blog', alert=alert))

        blog_id = str(generate_blog_id())
        blog = Blog(blog_id=blog_id, account=test_account.get_user_id(), blog_subject=create_blog_form.post_name.data,
                    image=filepath, blog_content=create_blog_form.post_content.data,
                    category=create_blog_form.category.data, upvote_count=0)

        blogs_dict[blog.get_blog_id()] = blog
        db['Blogs'] = blogs_dict

        # Test codes
        blogs_dict = db['Blogs']
        blog = blogs_dict[blog.get_blog_id()]
        print("Blog with ID", blog.get_blog_id(), "was stored in report_and_blog.db successfully")
        db.close()

        return redirect(url_for('retrieve_blogs'))
    return render_template('createBlog.html', form=create_blog_form)


@app.route('/searchBlog', methods=['GET', 'POST'])
def search_blog():
    search_blog_form = SearchBlogForm(request.form)
    create_comment_form = CreateCommentForm(request.form)
    blogs_dict = {}
    blogs_temp_dict = {}
    db = shelve.open('report_and_blog.db', 'c')
    try:
        blogs_dict = db['Blogs']
        blogs_temp_dict = db['Temp_Blogs']
    except:
        print("Error in retrieving Blog from report_and_blog.db.")

    count = 0
    if request.method == 'POST' and search_blog_form.validate():

        searched_post_name = search_blog_form.post_name.data
        searched_post_name_length = len(searched_post_name)
        print(blogs_temp_dict)
        blogs_list = []

        if searched_post_name is None: # checks if user wants to see all blogs
            for key in blogs_dict:
                blog = blogs_dict.get(key)
                blogs_list.append(blog)
        else:
            for key in blogs_dict:
                blog = blogs_dict.get(key)
                blog_post_name = blog.get_post_name()
                if blog_post_name[0:searched_post_name_length] == searched_post_name[0:searched_post_name_length]:
                    blogs_list.append(blog)

        # saves into temporary database
        blogs_temp_dict['temp_list'] = blogs_list
        db['Temp_Blogs'] = blogs_temp_dict
        print(blogs_temp_dict)
        db.close()

        paginated_info = paginate(request.args.get('page', 1, type=int), blogs_list, blogs_temp_dict['temp_list'])

        return render_template('searchBlog.html', comment_form=create_comment_form,
        form=search_blog_form, blogs_per_page=paginated_info[0], total_pages=paginated_info[1], page=paginated_info[2])

    else:

        blogs_temp_dict = db['Temp_Blogs']
        blogs_list = blogs_temp_dict['temp_list']
        print(blogs_list)

        paginated_info = paginate(request.args.get('page', 1, type=int), blogs_list, blogs_temp_dict['temp_list'])

        return render_template('searchBlog.html', comment_form=create_comment_form,
        form=search_blog_form, blogs_per_page=paginated_info[0], total_pages=paginated_info[1], page=paginated_info[2])

@app.route('/searchBlog', methods=['GET', 'POST'])
def retrieve_and_display_comments():
    create_comment_form = CreateCommentForm(request.form)

@app.route('/allBlogs')
def retrieve_blogs():
    blogs_dict = {}
    db = shelve.open('report_and_blog.db', 'r')
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
        db = shelve.open('report_and_blog.db', 'w')
        blogs_dict = db['Blogs']

        blog = blogs_dict.get(str(id))

        # remove old image from static/files and change to new picture

        img = request.files.getlist('image')[0]
        new_filepath = generate_image_id(img)
        old_filepath = blog.get_image()

        if new_filepath is not None:
            if new_filepath:
                img.save(new_filepath)  # save new filepath from static/files if not None
            else:
                alert = 'true'
                return redirect(url_for('update_blog', id=id, alert=alert))
        if old_filepath is not None:
            os.remove(old_filepath)  # remove old filepath from static/files if not None

        blog.set_post_name(update_blog_form.post_name.data)
        blog.set_image(new_filepath)
        blog.set_post_content(update_blog_form.post_content.data)
        blog.set_category(update_blog_form.category.data)

        db['Blogs'] = blogs_dict
        db.close()

        return redirect(url_for('retrieve_blogs'))
    else:
        blogs_dict = {}
        db = shelve.open('report_and_blog.db', 'r')
        blogs_dict = db['Blogs']
        db.close()

        blog = blogs_dict.get(str(id))
        update_blog_form.post_name.data = blog.get_post_name()
        update_blog_form.image.data = blog.get_image()
        update_blog_form.post_content.data = blog.get_post_content()
        update_blog_form.category.data = blog.get_category()

        return render_template('updateBlog.html', form=update_blog_form)


@app.route('/deleteBlog/<int:id>', methods=['POST'])
def delete_blog(id):
    blogs_dict = {}
    db = shelve.open('report_and_blog.db', 'w')
    blogs_dict = db['Blogs']

    blog_to_be_deleted = blogs_dict[str(id)]
    image_path = blog_to_be_deleted.get_image()
    if image_path is not None:
        os.remove(image_path)

    blogs_dict.pop(str(id))

    db['Blogs'] = blogs_dict
    db.close()

    session['blog_deleted'] = f'Blog ID: {blog_to_be_deleted.get_blog_id()} deleted.'

    return redirect(url_for('retrieve_blogs'))


@app.route('/reportedSubmitted', methods=['GET'])
def report_confirmed():
    return render_template('reportSubmitted.html')


@app.route('/reportCustomer', methods=['GET', 'POST'])
def submit_report():
    create_report_form = CreateReportForm(request.form)
    if request.method == 'POST' and create_report_form.validate():

        reports_dict = {}
        db = shelve.open('report_and_blog.db', 'c')
        try:
            reports_dict = db['Reports']
            blogs_dict = db['Blogs']
        except:
            print("Error in retrieving Blog from report_and_blog.db.")

        # create test account & generate random id with randint
        random_id = str(randint(1, 1000000))
        test_account = User()
        test_account.set_user_id(random_id)

        if check_report_id(create_report_form.reported_account.data) is False:
            alert = 'true'
            return redirect(url_for('submit_report', alert=alert))

        report = Report(account=None, reported_blog_id=create_report_form.reported_account.data,
                        reported_subjects=create_report_form.report_subjects.data,
                        report_reason=create_report_form.report_reason.data)

        reports_dict[report.get_report_id()] = report
        db['Reports'] = reports_dict

        # Test codes
        reports_dict = db['Reports']
        report = reports_dict[report.get_report_id()]
        print(report.get_report_id(), "was stored in report_and_blog.db successfully")
        db.close()

        return redirect(url_for('report_confirmed'))
    return render_template('reportCustomer.html', form=create_report_form)


@app.route('/unresolvedReports')
def retrieve_reports():
    reports_dict = {}
    db = shelve.open('report_and_blog.db', 'r')
    reports_dict = db['Reports']
    db.close()

    reports_list = []
    for key in reports_dict:
        report = reports_dict.get(key)
        reports_list.append(report)

    return render_template('unresolvedReports.html', count=len(reports_list), reports_list=reports_list)


if __name__ == '__main__':
    app.run()
