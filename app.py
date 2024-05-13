from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import pymysql

app=Flask(__name__)
app.secret_key='8563'

def get_db_connection():
    connection = pymysql.connect(host='192.168.0.10',
                                         user='leegisker',
                                         password='8563',
                                         db='SOP',
                                         charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor)
    return connection

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM SOP')
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', items=items)

@app.route('/api/password', methods=['GET'])
def get_password():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM SOP')
    passwords = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(passwords)

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'usuario_predeterminado' and password == 'contraseña_predeterminada':
            session['logged_in']=True
            return redirect(url_for('show_passwords'))
        else:
            return render_template('login.html', error='Credenciales incorrectas')
    return render_template('login.html')


    
    
@app.route('/logout')
def logout():
    session['logged_in']=False
    return redirect(url_for('login'))


@app.route('/add_password',methods=['POST','GET'])
def add_password():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method=='POST':
        website = request.form['website']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO passwords (website, password) VALUES (%s, %s)', (website, password))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('show_passwords'))
    return render_template('add_password.html')

@app.route('/show_passwords')
def show_passwords():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT website, password FROM passwords')
    passwords = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('show_passwords.html', passwords=passwords)
    
        
if __name__=='__main__':
    app.run(host='0.0.0.0',port=8080 )
      