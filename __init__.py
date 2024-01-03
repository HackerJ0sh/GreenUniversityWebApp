from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def cust_homepage():
    return render_template('customerHomepage.html')


if __name__ == '__main__':
    app.run()