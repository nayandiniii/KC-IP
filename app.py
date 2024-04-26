# app.py
import os  # Add this import
from flask import Flask, jsonify, render_template, request, redirect, url_for, session, send_file
from flask_mysqldb import MySQL
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import pandas as pd
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static\images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}


app = Flask(__name__)
app.secret_key = 'kcip2024'

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'nsn0407'
app.config['MYSQL_DB'] = 'kc_ip'

# Configure upload folder and allowed extensions
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS


mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/leads_form')
def leads_form():
    return render_template('leads_form.html')


@app.route('/lead_submit', methods=['POST'])
def lead_submit():
    if request.method == 'POST':
        representative_name = request.form['representative-name']
        mention_lead = request.form['mention-lead']
        contact_no = request.form['contact-no']
        address = request.form['address']
        state = request.form['state']
        type_of_lead = request.form['type-of-lead']
        additional_remarks = request.form['additional-remarks']

        # Insert data into MySQL database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO leads_details (representative_name, mention_lead, contact_no, address, state, type_of_lead, additional_remarks) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (representative_name, mention_lead, contact_no, address, state, type_of_lead, additional_remarks))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('leads_form'))
    else:
        return render_template('leads_form.html')


@app.route('/invoice_form', methods=['GET', 'POST'])
def invoice_form():
    if request.method == 'POST':
        # Fetch data from the form
        date_str = request.form['date']
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
        state=request.form['state']
        complementary_course_details = request.form['complementary-course-details']
        

       # Handle image upload
        if 'image' in request.files:
            image_file = request.files['image']  # Corrected key name
            if image_file.filename != '':
                # Save the image to the static folder
                image_filename = secure_filename(image_file.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
                image_file.save(image_path)
                # Save the image location in the database
                image_location = os.path.join('images', image_filename)  # Relative path
            else:
                image_location = None
        else:
            image_location = None

        # Insert data into MySQL database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO invoice_details (date, lead_source, lead_month, pre_enrollment_number, about_customer, batch_details, pitching_model, father_name, mother_name, student_name, student_age, current_address, school_name, contact_number, alternative_number, email, course, level, class_type, total_amount, amount_paid, payment_mode, emi_tenure, emi_per_month, course_duration, sales_consultant_name, department, complementary_course, language, demo_done, complementary_course_details,image_location, state) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)",
                    (date, lead_source, lead_month, pre_enrollment_number, about_customer, batch_details, pitching_model, father_name, mother_name, student_name, student_age, current_address, school_name, contact_number, alternative_number, email, course, level, class_type, total_amount, amount_paid, payment_mode, emi_tenure, emi_per_month, course_duration, sales_consultant_name, department, complementary_course, language, demo_done, complementary_course_details,image_location,state))
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
        user_data = cur.fetchone()  # Fetch the user details
        cur.close()

        if user_data:
            session['email'] = email
            kc_id = user_data[5]  # Access the KCID column by its index (assuming it's the sixth column)
            if kc_id and kc_id.startswith('KCE'):
                return redirect(url_for('form'))
            elif kc_id and kc_id.startswith('KCS'):
                return redirect(url_for('dashboard_student'))
            elif kc_id and kc_id.startswith('admin'):
                return redirect(url_for('admin_panel'))
            elif kc_id and kc_id.startswith('KCM'):
                return redirect(url_for('dashboard_mentor'))
            else:
                error = 'Invalid KC ID prefix'
                return render_template('login.html', error=error)
        else:
            error = 'Invalid email or password'
            return render_template('login.html', error=error)

    else:
        return render_template('login.html')
    

@app.route('/dashboard_mentor')
def dashboard_mentor():
    if 'email' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT kcid FROM user_details WHERE email = %s", (session['email'],))
        user_data = cur.fetchone()  # Fetch the user details
        if user_data:
            # Fetch mentor details based on email
            cur.execute("SELECT * FROM mentor_details WHERE email = %s", (session['email'],))
            mentor_details_data = cur.fetchone()
            mentor_details = dict(zip([column[0] for column in cur.description], mentor_details_data))
            
            cur.close()
            return render_template('dashboard_mentor.html', mentor_details=mentor_details)
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))



@app.route('/dashboard_student', methods=['GET', 'POST'])
def dashboard_student():
    user_details = None  # Assign a default value
    
    if 'email' in session:
        if request.method == 'POST':
            # Handle file upload and assignment of mentor
            if 'pdf_file' in request.files:
                pdf_file = request.files['pdf_file']

                if pdf_file.filename != '':
                    # Save the uploaded PDF file
                    pdf_filename = secure_filename(pdf_file.filename)
                    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
                    pdf_file.save(pdf_path)

                    # Get user details from session
                    email = session['email']
                    cur = mysql.connection.cursor()
                    cur.execute("SELECT name, kcid FROM user_details WHERE email = %s", (email,))
                    user_details = cur.fetchone()
                    name = user_details[0]
                    kcid = user_details[1]
                    cur.close()

                    # Store the PDF location, user details, and mentor details in the database
                    cur = mysql.connection.cursor()
                    cur.execute("INSERT INTO assignment (pdf_location, name, kcid) VALUES (%s, %s, %s)", (pdf_path, name, kcid))
                    mysql.connection.commit()
                    cur.close()

                    return redirect(url_for('dashboard_student'))

        cur = mysql.connection.cursor()
        cur.execute("SELECT kcid FROM user_details WHERE email = %s", (session['email'],))
        user_data = cur.fetchone()
        if user_data:
            kc_id = user_data[0]
            if kc_id and kc_id.startswith('KCS'):
                cur.execute("SELECT id, name FROM user_details WHERE kcid LIKE 'KCM%'")  # Fetch only names with kcid starting with KCM
                mentor_list = cur.fetchall()
                

                # Fetch invoice details
                cur.execute("SELECT * FROM invoice_details WHERE email = %s", (session['email'],))
                invoice_details_data = cur.fetchone()
                if invoice_details_data:
                    invoice_details = dict(zip([column[0] for column in cur.description], invoice_details_data))
                else:
                    invoice_details = {}

                cur.close()

                return render_template('dashboard_student.html', mentor_list=mentor_list, invoice_details=invoice_details, user_details=user_details)
            else:
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))




@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        contact = request.form['contact']
        email = request.form['email']
        kcid = request.form['kcid']
        password = request.form['password']
        
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
    
# Route to render dashboard.html
@app.route('/data_analysis')
def data_analysis():
    return render_template('data_analysis.html')

# Route to fetch data for chart 1
@app.route('/api/chart1Data')
def chart1_data():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT state, COUNT(DISTINCT id) AS count FROM invoice_details GROUP BY state")
    data = cursor.fetchall()
    labels = [row[0] for row in data]
    counts = [row[1] for row in data]
    return jsonify(labels=labels, counts=counts)

# Route to fetch data for chart 2
@app.route('/api/chart2Data')
def chart2_data():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT course, COUNT(DISTINCT id) AS count FROM invoice_details GROUP BY course")
    data = cursor.fetchall()
    labels = [row[0] for row in data]
    counts = [row[1] for row in data]
    return jsonify(labels=labels, counts=counts)

# Route to fetch data for chart 3
@app.route('/api/chart3Data')
def chart3_data():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT sales_consultant_name, COUNT(DISTINCT id) AS count FROM invoice_details GROUP BY sales_consultant_name")
    data = cursor.fetchall()
    labels = [row[0] for row in data]
    counts = [row[1] for row in data]
    return jsonify(labels=labels, counts=counts)

# Route to fetch data for chart 4
@app.route('/api/chart4Data')
def chart4_data():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT type_of_lead, COUNT(*) AS count FROM leads_details GROUP BY type_of_lead")
    data = cursor.fetchall()
    labels = [row[0] for row in data]
    counts = [row[1] for row in data]
    return jsonify(labels=labels, counts=counts)

# Route to fetch data for chart 5
@app.route('/api/chart5Data')
def chart5_data():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT department, COUNT(DISTINCT id) AS count FROM invoice_details GROUP BY department")
    data = cursor.fetchall()
    labels = [row[0] for row in data]
    counts = [row[1] for row in data]
    return jsonify(labels=labels, counts=counts)

@app.route('/feedback')
def feedback_form():
    return render_template('feedback.html')

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    if request.method == 'POST':
        mentor_name = request.form['mentor_name']
        student_id = request.form['student_id']
        material_used = request.form['material_used']
        teaching_methods = request.form['teaching_methods']
        delivery_of_content = request.form['delivery_of_content']
        behavior_with_students = request.form['behavior_with_students']
        additional_remarks = request.form['additional_remarks']
        
        # Insert data into MySQL database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO feedback (mentor_name, student_id, material_used, teaching_methods, delivery_of_content, behavior_with_students, additional_remarks) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (mentor_name, student_id, material_used, teaching_methods, delivery_of_content, behavior_with_students, additional_remarks))
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('feedback_form'))
    

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
    

@app.route('/feedback_data')
def feedback_data():
    return render_template('feedback_data.html')

@app.route('/api/feedbackData')
def fetch_feedback_data():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM feedback")
    data = cur.fetchall()
    cur.close()

    # Convert the data into a list of dictionaries for JSON serialization
    feedback_data = []
    for row in data:
        feedback_data.append({
            'id': row[0],
            'mentor_name': row[1],
            'student_id': row[2],
            'material_used': row[3],
            'teaching_methods': row[4],
            'delivery_of_content': row[5],
            'behavior_with_students': row[6],
            'additional_remarks': row[7]
        })

    return jsonify(feedback_data)

@app.route('/download_excel')
def download_excel():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM feedback")
    data = cur.fetchall()
    cur.close()

    # Convert data to DataFrame
    df = pd.DataFrame(data, columns=['ID', 'Mentor Name', 'Student ID', 'Material Used', 'Teaching Methods', 'Delivery of Content', 'Behavior with Students', 'Additional Remarks'])

    # Create Excel file
    excel_file_path = 'feedback_data.xlsx'
    df.to_excel(excel_file_path, index=False)

    # Send the Excel file to the client
    return send_file(excel_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
