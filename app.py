# app.py

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

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
            else:
                error = 'Invalid KC ID prefix'
                return render_template('login.html', error=error)
        else:
            error = 'Invalid email or password'
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')


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

if __name__ == '__main__':
    app.run(debug=True)
