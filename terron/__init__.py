from flask import Flask, render_template, request, redirect, url_for
from Forms import CreateFeedbackForm
import shelve, Feedback

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/createFeedback', methods=['GET', 'POST'])
def create_feedback():
    create_feedback_form = CreateFeedbackForm(request.form)
    if request.method == 'POST' and create_feedback_form.validate():
        feedbacks_dict = {}
        db = shelve.open('feedback.db', 'c')

        try:
            feedbacks_dict = db['Feedbacks']
        except:
            print("Error in retrieving Feedbacks from feedback.db.")

        feedback = Feedback.Feedback(create_feedback_form.membership.data, create_feedback_form.remarks.data)
        feedbacks_dict[feedback.get_feedback_id()] = feedback
        db['Feedbacks'] = feedbacks_dict

        db.close()



        return redirect(url_for('thank_you'))
    return render_template('createFeedback.html', form=create_feedback_form)

@app.route('/viewFeedback')
def view_feedback():
    feedbacks_dict = {}
    db = shelve.open('feedback.db', 'r')
    feedbacks_dict = db['Feedbacks']
    db.close()

    feedbacks_list = []
    for key in feedbacks_dict:
        feedback = feedbacks_dict.get(key)
        feedbacks_list.append(feedback)
    return render_template('view_feedback.html',count=len(feedbacks_list), feedbacks_list=feedbacks_list)

@app.route('/thankyou')
def thank_you():

    return render_template('thankyou.html')

@app.route('/retrieveFeedbacks')
def retrieve_feedbacks():
    feedbacks_dict = {}
    db = shelve.open('feedback.db', 'r')
    feedbacks_dict = db['Feedbacks']
    db.close()

    feedbacks_list = []
    for key in feedbacks_dict:
        feedback = feedbacks_dict.get(key)
        feedbacks_list.append(feedback)

    return render_template('retrieveFeedbacks.html', count=len(feedbacks_list), feedbacks_list=feedbacks_list)


@app.route('/updateFeedback/<int:id>/', methods=['GET', 'POST'])
def update_feedback(id):
    update_feedback_form = CreateFeedbackForm(request.form)
    if request.method == 'POST' and update_feedback_form.validate():
        feedbacks_dict = {}
        db = shelve.open('feedback.db', 'w')
        feedbacks_dict = db['Feedbacks']

        feedback = feedbacks_dict.get(id)

        feedback.set_membership(update_feedback_form.membership.data)
        feedback.set_remarks(update_feedback_form.remarks.data)

        db['Feedbacks'] = feedbacks_dict
        db.close()

        return redirect(url_for('retrieve_feedbacks'))
    else:
        feedbacks_dict = {}
        db = shelve.open('feedback.db', 'r')
        feedbacks_dict = db['Feedbacks']
        db.close()

        feedback = feedbacks_dict.get(id)

        update_feedback_form.membership.data = feedback.get_membership()
        update_feedback_form.remarks.data = feedback.get_remarks()

        return render_template('updateFeedback.html', form=update_feedback_form)




@app.route('/deleteFeedback/<int:id>', methods=['POST'])
def delete_feedback(id):
    feedbacks_dict = {}
    db = shelve.open('feedback.db', 'w')
    feedbacks_dict = db['Feedbacks']

    feedbacks_dict.pop(id)

    db['Feedbacks'] = feedbacks_dict
    db.close()

    return redirect(url_for('retrieve_feedbacks'))

@app.route('/deleteFeedbackCustomer/<int:id>', methods=['POST'])
def delete_feedbackCustomer(id):
    feedbacks_dict = {}
    db = shelve.open('feedback.db', 'w')
    feedbacks_dict = db['Feedbacks']

    feedbacks_dict.pop(id)

    db['Feedbacks'] = feedbacks_dict
    db.close()

    return redirect(url_for('view_feedback'))

if __name__ == '__main__':
    app.run()