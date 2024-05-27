from flask import Flask, render_template, request, redirect, url_for, session
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def get_db_connection():
    connection = pymysql.connect(
        host='172.19.168.80',  # Reemplaza con la IP correcta de tu máquina
        user='leegisker',
        password='28sylaxl',
        db='password_manager',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
            user = cursor.fetchone()
        connection.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            return redirect(url_for('home'))
        else:
            error = 'Invalid email or password'
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            error = 'Passwords do not match'
        else:
            hashed_password = generate_password_hash(password)
            
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
                user = cursor.fetchone()
                
                if user:
                    error = 'Email already registered'
                else:
                    cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, hashed_password))
                    connection.commit()
                    return redirect(url_for('login'))
            connection.close()
    return render_template('register.html', error=error)

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/register_account', methods=['GET', 'POST'])
def register_account():
    error = None
    if request.method == 'POST':
        website = request.form['website']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO passwords (user_id, website, username, email, password) VALUES (%s, %s, %s, %s, %s)",
                           (session['user_id'], website, username, email, password))
            connection.commit()
        connection.close()
        return redirect(url_for('home'))
    return render_template('register_account.html', error=error)


@app.route('/view_accounts')
def view_accounts():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT website, username, email, password FROM passwords WHERE user_id=%s", (session['user_id'],))
        accounts = cursor.fetchall()
    connection.close()
    
    return render_template('view_accounts.html', accounts=accounts)

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
