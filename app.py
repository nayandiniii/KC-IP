# app.py

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'kcip2024'

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'nsn0407'
app.config['MYSQL_DB'] = 'kc_ip'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/leads_form')
def leads_form():
    return render_template('leads_form.html')


@app.route('/invoice_form', methods=['GET', 'POST'])
def invoice_form():
    if request.method == 'POST':
        # Fetch data from the form
        date_str = request.form['date']
# Assuming the date format is 'YYYY-MM-DD' in the form
        date = datetime.strptime(date_str, '%Y-%m-%d').date()        
        lead_source = request.form['lead-source']
        lead_month = request.form['lead-month']
        pre_enrollment_number = request.form['pre-enrollment-number']
        about_customer = request.form['about-customer']
        batch_details = request.form['batch-details']
        pitching_model = request.form['pitching-model']
        father_name = request.form['father-name']
        mother_name = request.form['mother-name']
        student_name = request.form['student-name']
        student_age = request.form['student-age']
        current_address = request.form['current-address']
        school_name = request.form['school-name']
        contact_number = request.form['contact-number']
        alternative_number = request.form['alternative-number']
        email = request.form['email']
        course = request.form['course']
        level = request.form['level']
        class_type = request.form['class-type']
        total_amount = request.form['total-amount']
        amount_paid = request.form['amount-paid']
        payment_mode = request.form['payment-mode']
        emi_tenure = request.form['emi-tenure']
        emi_per_month = request.form['emi-per-month']
        course_duration = request.form['course-duration']
        sales_consultant_name = request.form['sales-consultant-name']
        department = request.form['department']
        complementary_course = request.form['complementary-course']
        language = request.form['language']
        demo_done = request.form['demo-done']
        complementary_course_details = request.form['complementary-course-details']

        # Insert data into MySQL database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO invoice_details (date, lead_source, lead_month, pre_enrollment_number, about_customer, batch_details, pitching_model, father_name, mother_name, student_name, student_age, current_address, school_name, contact_number, alternative_number, email, course, level, class_type, total_amount, amount_paid, payment_mode, emi_tenure, emi_per_month, course_duration, sales_consultant_name, department, complementary_course, language, demo_done, complementary_course_details) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (date, lead_source, lead_month, pre_enrollment_number, about_customer, batch_details, pitching_model, father_name, mother_name, student_name, student_age, current_address, school_name, contact_number, alternative_number, email, course, level, class_type, total_amount, amount_paid, payment_mode, emi_tenure, emi_per_month, course_duration, sales_consultant_name, department, complementary_course, language, demo_done, complementary_course_details))
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('form'))
    else:
        return render_template('invoice_form.html')

    


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user_details WHERE email = %s AND password = %s", (email, password))
        user = cur.fetchone()
        cur.close()
        
        if user:
            session['email'] = email
            kc_id = user[5] if user else None  # Access the sixth element of the tuple if user exists
            if kc_id and kc_id.startswith('KCE'):
                return redirect(url_for('form'))
            elif kc_id and kc_id.startswith('KCS'):
                return redirect(url_for('dashboard'))
            elif kc_id and kc_id.startswith('admin'):
                return redirect(url_for('admin_panel'))
            else:
                error = 'Invalid KC ID prefix'
                return render_template('login.html', error=error)
        else:
            error = 'Invalid email or password'
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')


@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        contact = request.form['contact']
        email = request.form['email']
        kcid = request.form['kcid']
        password = request.form['password']
        recipient_email = request.form['recipient_email']  # Get recipient email from the form
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user_details (name, age, contact, email, kcid, password) VALUES (%s, %s, %s, %s, %s, %s)", (name, age, contact, email, kcid, password))
        mysql.connection.commit()
        cur.close()
        
        ''' Send email to user with their details
        sender_email = "nandini.kidschaupal@gmail.com"  # Change to your email address
        sender_password = "Nandini@7557"  # Change to your email password
        send_email_to_user(sender_email, sender_password, recipient_email, name, age, contact, kcid, password)  # Pass email to the function
        '''
        return redirect(url_for('admin_panel'))



'''
# Modify the send_email_to_user function to accept the recipient email as a parameter
# Modify the send_email_to_user function to accept the recipient email as a parameter
def send_email_to_user(sender_email, sender_password, recipient_email, name, age, contact, kcid, password):
    # Email body text
    body = f"""
    Hello New Joiner!

    Welcome to KidsChaupal. Here are your credentials for login:

    Email: {recipient_email}
    Password: {password}
    KC ID: {kcid}
    """

    # Create a message object
    message = MIMEText(body)

    # Set email headers
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = "User Details"

    # Connect to the SMTP server and send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message.as_string()) '''

@app.route('/mentor_details')
def mentor_details():
    return render_template('mentor_details.html')

@app.route('/mentor_submit', methods=['POST'])
def mentor_submit():
    if request.method == 'POST':
        mentor_name = request.form['mentor-name']
        birthdate = request.form['birthdate']
        email = request.form['email']
        address = request.form['address']
        state = request.form['state']
        education = request.form['education']
        highest_qualification = request.form['highest-qualification']
        certifications = request.form['certifications']
        course = request.form['course']
        level = request.form['level']
        expected_payment = request.form['expected-payment']
        available_slots = request.form['available-slots']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO mentor_details (mentor_name, birthdate, email, address, state, education, highest_qualification, certifications, course, level, expected_payment, available_slots) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (mentor_name, birthdate, email, address, state, education, highest_qualification, certifications, course, level, expected_payment, available_slots))
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('mentor_details'))
    else:
        return render_template('mentor_details.html')
    


@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        return render_template('dashboard.html', email=session['email'])
    else:
        return redirect(url_for('login'))

@app.route('/form')
def form():
    if 'email' in session:
        return render_template('form.html')
    else:
        return redirect(url_for('login'))

@app.route('/admin_panel')
def admin_panel():
    if 'email' in session:
        return render_template('admin_panel.html')
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
