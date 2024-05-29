from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymysql

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def get_db_connection():
    connection = pymysql.connect(
        host='db',
        user='leegisker',
        password='28sylaxl',
        db='password_manager',
        port=3306,
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
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
                user = cursor.fetchone()
                if user:
                    session['user_id'] = user['id']
                    return redirect(url_for('home'))
                else:
                    error = 'Invalid email or password'
        finally:
            connection.close()
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
                user = cursor.fetchone()
                if user:
                    error = 'Email already registered'
                else:
                    cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
                    connection.commit()
                    flash('Registration successful! Please login.', 'success')
                    return redirect(url_for('login'))
        finally:
            connection.close()
    return render_template('register.html', error=error)

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/test-db-connection')
def test_db_connection():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
        connection.close()
        
        # Generate HTML table
        table_html = "<table border='1'><tr><th>ID</th><th>Email</th><th>Password</th></tr>"
        for user in users:
            table_html += f"<tr><td>{user['id']}</td><td>{user['email']}</td><td>{user['password']}</td></tr>"
        table_html += "</table>"

        return f"Connected to the database. Users table:<br>{table_html}"
    except pymysql.MySQLError as e:
        return f"Error connecting to the database: {str(e)}"

@app.route('/register_account', methods=['GET', 'POST'])
def register_account():
    error = None
    if request.method == 'POST':
        website = request.form['website']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            error = "Passwords do not match"
        else:
            connection = get_db_connection()
            try:
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO passwords (user_id, website, username, email, password) VALUES (%s, %s, %s, %s, %s)",
                                   (session['user_id'], website, username, email, password))
                    connection.commit()
                    return redirect(url_for('home'))
            except pymysql.MySQLError as e:
                error = f"An error occurred: {e}"
            finally:
                connection.close()
    return render_template('register_account.html', error=error)


@app.route('/view_accounts')
def view_accounts():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM passwords WHERE user_id=%s", (session['user_id'],))
        accounts = cursor.fetchall()
    connection.close()
    return render_template('view_accounts.html', accounts=accounts)

@app.route('/edit_account/<int:account_id>', methods=['GET', 'POST'])
def edit_account(account_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM passwords WHERE id=%s AND user_id=%s", (account_id, session['user_id']))
        account = cursor.fetchone()
    
    if request.method == 'POST':
        website = request.form['website']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("UPDATE passwords SET website=%s, username=%s, email=%s, password=%s WHERE id=%s AND user_id=%s",
                               (website, username, email, password, account_id, session['user_id']))
                connection.commit()
                return redirect(url_for('view_accounts'))
        except pymysql.MySQLError as e:
            error = f"An error occurred: {e}"
        finally:
            connection.close()
    return render_template('edit_account.html', account=account, error=error)

@app.route('/delete_account/<int:account_id>', methods=['POST'])
def delete_account(account_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM passwords WHERE id=%s AND user_id=%s", (account_id, session['user_id']))
            connection.commit()
        flash('Account deleted successfully', 'success')
    except pymysql.MySQLError as e:
        flash(f"An error occurred: {e}", 'danger')
    finally:
        connection.close()
    return redirect(url_for('view_accounts'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
