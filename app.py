# app.py

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
