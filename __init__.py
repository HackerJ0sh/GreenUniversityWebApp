from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

from blogForm import CreateBlogForm
import shelve
from formClasses import *
from reportForm import CreateReportForm
from random import randint
import os

app = Flask(__name__, template_folder='customerTemplates')
app.config['UPLOAD_FOLDER'] = 'static/files'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'png'}
app.secret_key = 'fuck this shitty project'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


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

        blog = Blog(account=test_account.get_user_id(), blog_subject=create_blog_form.post_name.data,
            image=create_blog_form.image.data, blog_content=create_blog_form.post_content.data,
            category=create_blog_form.category.data, upvote_count=0)

        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            print(f'Image successfully uploaded and saved; file path: {filepath}')

        else:
            print('Allowed image types are - png and jpg')

        blogs_dict[blog.get_blog_id()] = blog
        db['Blogs'] = blogs_dict

        # Test codes
        blogs_dict = db['Blogs']
        blog = blogs_dict[blog.get_blog_id()]
        print("Blog with ID", blog.get_blog_id(), "was stored in report_and_blog.db successfully")
        db.close()

        return redirect(url_for('retrieve_blogs'))
    return render_template('createBlog.html', form=create_blog_form)


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
        db = shelve.open('report_and_blog.db', 'r')
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
    db = shelve.open('report_and_blog.db', 'w')
    blogs_dict = db['Blogs']
    blogs_dict.pop(id)
    db['Blogs'] = blogs_dict
    db.close()

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
        except:
            print("Error in retrieving Blog from report_and_blog.db.")

        # create test account & generate random id with randint
        random_id = str(randint(1, 1000000))
        test_account = User()
        test_account.set_user_id(random_id)

        report = Report(account=None, reported_account_id=create_report_form.reported_account.data,
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



