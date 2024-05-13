from flask import Flask, render_template, request, jsonify
import pymysql
app=Flask(__name__)

def get_db_connection():
    connection = pymysql.connector.connect(host='192.168.0.10',
                                         user='leegisker',
                                         password='8563',
                                         db='sop',
                                         charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor)
    return connection

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sop')
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', items=items)

@app.route('/api/password', methods=['GET'])
def get_password():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sop')
    passwords = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(passwords)

if __name__=='__main__':
    app.run(host='0.0.0.0',port=8080 )
      