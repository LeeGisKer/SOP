from flask import Flask, render_template
import pymysql
app=Flask(__name__)

def get_db_connection():
    connection = pymysql.connector.connect(host='localhost',
                                         user='root,',
                                         password='1234',
                                         db='sop')
    return connection


@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sop')
    items = cursor.fetchall()
    conn.close()
    return render_template('index.html', items=items)

if __name__=='__main__':
    app.run(host='0.0.0.0',port=8080 )
      