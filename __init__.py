from flask import Flask, render_template, request, redirect, url_for
from BlogForm import CreateBlogForm

app = Flask(__name__, template_folder='customerTemplates')


@app.route('/')
def homepage():
    return render_template('customerHomepage.html')


@app.route('/createBlog', methods=['GET', 'POST'])
def create_user():
    create_blog_form = CreateBlogForm(request.form)
    if request.method == 'POST' and create_blog_form.validate():
        return redirect(url_for('home'))
    return render_template('createBlog.html', form=create_blog_form)


if __name__ == '__main__':
    app.run()




