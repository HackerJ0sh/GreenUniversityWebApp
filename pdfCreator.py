from random import randint

from fpdf import FPDF


class PDFExporter(FPDF):
    def __init__(self, date_created, generated_by):
        super().__init__()
        self.date_created = date_created
        self.generated_by = generated_by

    def sample_header(self, header):
        """Creates a sample header with title, author, and subject."""
        self.set_font("Helvetica", size=16, style="B")
        self.cell(200, 10, txt=f"Green University Status Report: {header}", ln=1)
        self.set_font("Helvetica", size=8, style="I")
        self.cell(200, 10, txt=f"Generated as of {self.date_created} by staff with ID: {self.generated_by}")

    def add_blog_data_page(self, data):
        data = data
        dict_of_categories = {'Others': 0, 'Recycling': 0, 'Sustainability': 0, 'Business': 0, 'Water': 0, 'Cultural': 0}
        blogs = data['Blogs']
        reports = data['Reports']
        """Adds a page with title and specified data."""
        self.add_page()
        self.sample_header('Blogs')
        self.set_font("Helvetica", size=12)
        self.set_y(30)  # Set starting y position after header

        # get number of instances in the dataset
        self.cell(10, 5, txt=f"There are currently {len(blogs)} blogs and {len(reports)} reports", ln=1)

        # find the number of blogs of different categories
        self.cell(10, 5, txt="-----------------------------------------", ln=1)
        self.set_font("Helvetica", size=10, style="U")
        self.cell(10, 5, txt=f"Of the {len(blogs)} blogs (identify most posted category): ", ln=1)
        self.set_font("Helvetica", size=10)
        for key in blogs:
            blog = blogs.get(key)
            categories = blog.get_category()
            for category in categories:
                if category == 'ETC':
                    dict_of_categories['Others'] += 1
                elif category == 'REC':
                    dict_of_categories['Recycling'] += 1
                elif category == 'SSB':
                    dict_of_categories['Sustainability'] += 1
                elif category == 'BIZ':
                    dict_of_categories['Business'] += 1
                elif category == 'H20':
                    dict_of_categories['Water'] += 1
                elif category == 'CUL':
                    dict_of_categories['Cultural'] += 1
        self.cell(10, 5, txt=f"{dict_of_categories['Others']} are categorized as 'Others' ", ln=1)
        self.cell(10, 5, txt=f"{dict_of_categories['Recycling']} are categorized as 'Recycling' ", ln=1)
        self.cell(10, 5, txt=f"{dict_of_categories['Sustainability']} are categorized as 'Sustainability' ", ln=1)
        self.cell(10, 5, txt=f"{dict_of_categories['Business']} are categorized as 'Business' ", ln=1)
        self.cell(10, 5, txt=f"{dict_of_categories['Water']} are categorized as 'Water' ", ln=1)
        self.cell(10, 5, txt=f"{dict_of_categories['Cultural']} are categorized as 'Cultural' ", ln=1)
        most_categories = max(dict_of_categories, key=dict_of_categories.get)
        self.cell(10, 5, txt=f"Therefore, it can be concluded that the most posted category is {most_categories}", ln=1)

        # print comments per blogs
        self.cell(10, 5, txt="-----------------------------------------", ln=1)
        self.set_font("Helvetica", size=10, style="U")
        self.cell(10, 5, txt=f"Of the {len(blogs)} blogs (identify blog with the most comments): ", ln=1)
        self.set_font("Helvetica", size=10)
        max_comments = 0
        blog_with_most_comments = None
        for key in blogs:
            blog = blogs.get(key)
            comments = blog.get_comments()
            if len(comments) > max_comments:
                max_comments = len(comments)
                blog_with_most_comments = blog.get_blog_id()
            self.cell(10, 5, txt=f"Blog {blog.get_blog_id()} has {len(comments)} comments.", ln=1)
        self.cell(10, 5, txt=f"Therefore, it can be concluded that the blog with the most comments is:"
         f" Blog {blog_with_most_comments} - {max_comments} comments", ln=1)

    def add_product_data_page(self, data):
        data = data
        products = data['Products']

        self.add_page()
        self.sample_header('Products')
        self.set_font("Helvetica", size=12)
        self.set_y(30)  # Set starting y position after header

        # get number of instances in the dataset
        self.cell(10, 5, txt=f"There are currently {len(products)} products", ln=1)

        # find the quantity of products per product
        self.cell(10, 5, txt="-----------------------------------------", ln=1)
        self.set_font("Helvetica", size=10, style="U")
        self.cell(10, 5, txt=f"Of the {len(products)} products (identify product with highest quantity): ", ln=1)
        self.set_font("Helvetica", size=10)
        max_quantity = 0
        product_with_highest_quantity = None
        for key in products:
            product = products.get(key)
            product_name = product.get_product_name()
            product_id = product.get_product_id()
            product_quantity = product.get_quantity()
            if product_quantity > max_quantity:
                max_quantity = product_quantity
                product_with_highest_quantity = f'{product_id} ({product_name})'
            self.cell(10, 5, txt=f"Product {product_id} ({product_name}) has {product_quantity} in stock.", ln=1)
        self.cell(10, 5, txt=f"Therefore, it can be concluded that the product with the highest quantity is:"
         f" Product {product_with_highest_quantity} - {max_quantity} in stock", ln=1)

        # find the product prices
        self.cell(10, 5, txt="-----------------------------------------", ln=1)
        self.set_font("Helvetica", size=10, style="U")
        self.cell(10, 5, txt=f"Of the {len(products)} products (identify product with highest potential [price x quantity]): ", ln=1)
        self.set_font("Helvetica", size=10)
        max_potential = 0
        product_with_highest_potential = None
        for key in products:
            product = products.get(key)
            product_name = product.get_product_name()
            product_id = product.get_product_id()
            product_quantity = product.get_quantity()
            product_price = product.get_product_price()
            product_potential =  product_quantity * product_price
            if product_potential > max_potential:
                max_potential = product_potential
                product_with_highest_potential = f'{product_id} ({product_name})'
            self.cell(10, 5, txt=f"Product {product_id} ({product_name})'s potential"
            f" is {product_potential} SGD [{product_price} (Price) x {product_quantity} (Quantity)", ln=1)
        self.cell(10, 5, txt=f"Therefore, it can be concluded that the product with the highest quantity is:"
                             f" Product {product_with_highest_potential} - {max_potential} SGD", ln=1)

    def add_account_data_page(self, data):
        data = data
        users = data['Users']

        self.add_page()
        self.sample_header('Accounts')
        self.set_font("Helvetica", size=12)
        self.set_y(30)  # Set starting y position after header

        # get number of instances in the dataset
        self.cell(10, 5, txt=f"There are currently {len(users)} accounts.", ln=1)

        # find the ratio of staff accounts to customer accounts
        self.cell(10, 5, txt="-----------------------------------------", ln=1)
        self.set_font("Helvetica", size=10, style="U")
        self.cell(10, 5, txt=f"Of the {len(users)} accounts (identify ratio of staff/customer accounts): ", ln=1)
        self.set_font("Helvetica", size=10)

        staff_accs = 0
        cust_accs = 0
        for key in users:
            user = users.get(key)
            account_id = user.get_user_id()
            account_name = user.get_name()
            account_type = user.get_account_type()
            if account_type == 'C':
                account_type = 'Customer'
                cust_accs +=1
            elif account_type == 'S':
                account_type = 'Staff'
                staff_accs += 1
            self.cell(10, 5, txt=f"Account {account_id} ({account_name}) is a {account_type} account. ", ln=1)
        self.cell(10, 5, txt=f"Therefore, it can be concluded that the ratio of staff to customer accounts is"
              f"({staff_accs} (Staff Accounts): {cust_accs} (Customer Accounts)", ln=1)

        # find the ratio of locked accounts to unlocked accounts
        self.cell(10, 5, txt=f"There are currently {len(users)} accounts.", ln=1)

        # find the ratio of staff accounts to customer accounts
        self.cell(10, 5, txt="-----------------------------------------", ln=1)
        self.set_font("Helvetica", size=10, style="U")
        self.cell(10, 5, txt=f"Of the {len(users)} accounts (identify ratio of locked/unlocked accounts): ", ln=1)
        self.set_font("Helvetica", size=10)

        locked_accs = 0
        unlocked_accs = 0
        for key in users:
            user = users.get(key)
            account_id = user.get_user_id()
            account_name = user.get_name()
            account_status = user.get_account_status()
            if account_status == 'L':
                account_status = 'Locked'
                locked_accs +=1
            elif account_status == 'U':
                account_status = 'Unlocked'
                unlocked_accs += 1
            self.cell(10, 5, txt=f"Account {account_id} ({account_name}) is {account_status}. ", ln=1)
        self.cell(10, 5, txt=f"Therefore, it can be concluded that the ratio of locked to unlocked accounts is"
              f"({locked_accs} (Staff Accounts): {unlocked_accs} (Customer Accounts)", ln=1)

    def add_payment_data_page(self, data):
        data = data
        payment = data['Payments']

        self.add_page()
        self.sample_header('Payment Details')
        self.set_font("Helvetica", size=12)
        self.set_y(30)  # Set starting y position after header

        # get number of instances in the dataset
        self.cell(10, 5, txt=f"There are currently {len(payment)} payment details.", ln=1)

        # display payment details
        self.cell(10, 5, txt="-----------------------------------------", ln=1)

        self.set_font("Helvetica", size=10)
        for key in payment:
            payment_detail = payment.get(key)
            payment_id = payment_detail.get_id()
            full_name = payment_detail.get_full_name()
            user_id = payment_detail.get_user_id()
            email = payment_detail.get_email()
            phone_number = payment_detail.get_phone_number()
            self.cell(10, 5, txt=f"-------------------PAYMENT DETAILS FOR PAYMENT DETAIL {payment_id}-------------------", ln=1)
            self.cell(10, 5, txt=f"Full Name: {full_name}", ln=1)
            self.cell(10, 5, txt=f"User ID: {user_id}", ln=1)
            self.cell(10, 5, txt=f"Phone Number: {phone_number}", ln=1)
            self.cell(10, 5, txt=f"Email: {email}", ln=1)
            self.cell(10, 5,
                      txt=f"-------------------------------------------------------------------------------------", ln=1)

    def add_feedback_data_page(self, data):
        data = data
        all_feedback = data['Feedbacks']

        self.add_page()
        self.sample_header('Feedback')
        self.set_font("Helvetica", size=12)
        self.set_y(30)  # Set starting y position after header

        # get number of instances in the dataset
        self.cell(10, 5, txt=f"There are currently {len(all_feedback)} feedback.", ln=1)

        # display feedback details
        for key in all_feedback:
            feedback = all_feedback.get(key)
            feedback_id = feedback.get_feedback_id()
            feedback_satisfaction = feedback.get_membership()
            feedback_remarks = feedback.get_remarks()
            if feedback_remarks == "B":
                feedback_remarks = 'Bad'
            elif feedback_remarks == "N":
                feedback_remarks = "Neutral"
            elif feedback_remarks == "G":
                feedback_remarks = "Good"
            self.cell(10, 5, txt=f"-------------------FEEDBACK FOR FEEDBACK {feedback_id}-------------------", ln=1)
            self.set_font("Helvetica", size=10)
            self.cell(10, 5, txt=f"Satisfaction Level: {feedback_satisfaction}", ln=1)
            self.cell(10, 5, txt=f"Feedback Remarks: {feedback_remarks}", ln=1)



    def export_pdf(self):
        generate_pdf_id = randint(10 ** 14, 10 ** 15)
        self.output(f'static/reports/{generate_pdf_id}GU_progress_report.pdf')
        return generate_pdf_id


