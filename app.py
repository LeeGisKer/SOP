from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_bcrypt import Bcrypt
import pymysql

app=Flask(__name__)
Bcrypt = Bcrypt(app)
app.secret_key='8563'

def get_db_connection():
    connection = pymysql.connect(host='192.168.243.48',
                                         user='leegisker',
                                         password='8563',
                                         db='SOP',
                                         charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor)
    return connection

 

@app.route('/')
def index():
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM SOP')
                items = cursor.fetchall()
                return render_template('index.html', items=items)
        except pymysql.Error as e:
            app.logger.error(f"ERROR: {e}")
            return render_template('error.html')
        finally:
            conn.close()
    else:
        return render_template('error.html')
    
    
    
    
    
   

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
    if request.method=='POST' and request.form['username']=='usuario_predeterminado' and request.form['password']=='contraseña_predeterminada':
        session['logged_in']=True
        return redirect(url_for('show_passwords'))
    return render_template('login.html', error=request.method=='POST')



    
    
@app.route('/logout')
def logout():
    session['logged_in']=False
    return redirect(url_for('login'))


@app.route('/add_password',methods=['POST','GET'])
def add_password():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    website = request.form['website']
    password = request.form['password']
    
    if not website or not password:
        return render_template('error.html',message='Todos los campos son obligatorios')
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute('INSERT INTO passwords (website, password) VALUES (%s, %s)', (website, hashed_password))
                conn.commit()
                return redirect(url_for('show_passwords'))
        except pymysql.Error as e:
            app.logger.error(f"ERROR: {e}")
            return render_template('error.html')
        finally:
            conn.close()
    else:
        return render_template('error.html')
    
    

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
    
try:
    conn=get_db_connection()
    cursor=conn.cursor()
    cursor.execute('SELECT * FROM SOP')
    items=cursor.fetchall()
except Exception as e:
    print(f"ERROR: {e}")
    items=[]
finally:
    cursor.close()
        
    
 
        
if __name__=='__main__':
    app.run(host='0.0.0.0',port=8080 )
      