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
        user_data = cur.fetchone()
        if user_data:
            cur.execute("SELECT * FROM mentor_details WHERE email = %s", (session['email'],))
            mentor_details_data = cur.fetchone()
            mentor_details = dict(zip([column[0] for column in cur.description], mentor_details_data))
            cur.close()
            if mentor_details:
                # Fetch the mentor's ID from user_details table based on the email in session
                cur = mysql.connection.cursor()
                cur.execute("SELECT kcid FROM user_details WHERE email = %s", (session['email'],))
                mentor_id_data = cur.fetchone()
                if mentor_id_data:
                    mentor_id = mentor_id_data[0]  # Assuming mentor_id is in the first column
                    print(mentor_id)
                    cur.execute("SELECT pdf_location, name, kcid FROM assignment WHERE mentor_id = %s", (mentor_id,))
                    assignment_details_data = cur.fetchall()
                    assignment_details = []
                    for row in assignment_details_data:
                        assignment_details.append(dict(zip([column[0] for column in cur.description], row)))
                    cur.close()

                    return render_template('dashboard_mentor.html', mentor_details=mentor_details, assignment_details=assignment_details)
                else:
                    return "Mentor ID not found"
            else:
                return "Mentor details not found"
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))




@app.route('/delete_assignment', methods=['POST'])
def delete_assignment():
    if 'email' in session:
        if request.method == 'POST':
            assignment_id = request.form['assignment_id']
            assignment_loc = request.form['assignment_loc']

            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM assignment WHERE kcid = %s and name = %s", (assignment_id, assignment_loc))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('dashboard_mentor'))
    return redirect(url_for('login'))



@app.route('/dashboard_student', methods=['GET', 'POST'])
def dashboard_student():
    user_details = None
    invoice_details = None

    if 'email' in session:
        if request.method == 'POST':
            if 'pdf_file' in request.files:
                pdf_file = request.files['pdf_file']
                mentor_name = request.form['mentor_name']
                mentor_id = request.form['mentor_id']
                
                if pdf_file.filename != '':
                    pdf_filename = secure_filename(pdf_file.filename)
                    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
                    pdf_file.save(pdf_path)
                    pdf_location = 'images/' + pdf_filename  # Manually construct the file location with forward slashes


                    # Fetch user details for assignment
                    user_email = session['email']
                    cur = mysql.connection.cursor()
                    cur.execute("SELECT name, kcid FROM user_details WHERE email = %s", (user_email,))
                    user_details = cur.fetchone()
                    if user_details:
                        name, kcid = user_details
                        cur.close()

                        # Insert assignment details into the database
                        cur = mysql.connection.cursor()
                        cur.execute("INSERT INTO assignment (pdf_location, name, kcid, mentor_name, mentor_id) VALUES (%s, %s, %s, %s, %s)", 
                                    (pdf_location, name, kcid, mentor_name, mentor_id))
                        mysql.connection.commit()
                        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT kcid FROM user_details WHERE email = %s", (session['email'],))
        user_data = cur.fetchone()  # Fetch the user details
        if user_data:
            kc_id = user_data[0] 
            print(kc_id) # Access the KCID column by its index
            if kc_id and kc_id.startswith('KCS'):
                # Fetch user details and invoice details based on email
                cur.execute("SELECT * FROM user_details WHERE email = %s", (session['email'],))
                user_details_data = cur.fetchone()
                user_details = dict(zip([column[0] for column in cur.description], user_details_data))
                
                cur.execute("SELECT * FROM invoice_details WHERE email = %s", (session['email'],))
                invoice_details_data = cur.fetchone()
                print(invoice_details_data)
                invoice_details = dict(zip([column[0] for column in cur.description], invoice_details_data))
                
                cur.close()
                return render_template('dashboard_student.html', user_details=user_details, invoice_details=invoice_details)
            else:
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


# Route to handle downloading mentor list
@app.route('/download_mentor_list', methods=['POST'])
def download_mentor_list():
    # Fetch data from user_details and mentor_details tables
    cur = mysql.connection.cursor()
    cur.execute("SELECT user_details.name, user_details.email, user_details.kcid, user_details.contact, mentor_details.course FROM user_details INNER JOIN mentor_details ON user_details.email = mentor_details.email")
    data = cur.fetchall()
    cur.close()

    # Create DataFrame from fetched data
    df = pd.DataFrame(data, columns=['Name', 'Email', 'KCID', 'Contact', 'Course'])

    # Create Excel file
    excel_file_path = 'mentor_list.xlsx'
    df.to_excel(excel_file_path, index=False)

    # Return the Excel file as an attachment
    return send_file(excel_file_path, as_attachment=True)


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

