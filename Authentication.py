#from urllib import request
#import OpenSSL
from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

db_connection = mysql.connector.connect(user='root', password='12345', host='127.0.0.1', database='marlabs')
my_cursor = db_connection.cursor()

@app.route('/')
def home():
    return "Hello"
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_name = request.form.get('name')
        password = request.form.get('password')

        my_cursor.execute("insert into userdetails(username, user_pass) values(%s, %s)",(user_name, password))
        db_connection.commit()
        # db_connection.close()
        return 'Registered Suscessfully'
    return render_template('register.html')

@app.route('/data')
def fetch_data():
    my_cursor.execute('select * from userdetails')
    data = my_cursor.fetchall()
    return render_template('data.html', data = data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('name')
        pas = request.form.get('password')

        query = 'select username, user_pass from userdetails where username= %s and user_pass= %s'
        my_cursor.execute(query,(user, pas))
        data = my_cursor.fetchall()

        if len(data) == 1:
            return "<h1>SUCCESSFULLY LOGGED IN</h1>"
        else:
            return "<h1>REGISTER FIRST</h1>"
    return render_template('login.html')

@app.route('/change_pass', methods=['GET','POST'])
def change_pass():
    if request.method == 'POST':
        user = request.form.get('name')
        old_p = request.form.get('old_pass')
        new_p = request.form.get('new_pass')
        cnf_p = request.form.get('cnf_pass')


        if new_p == cnf_p:
            my_cursor.execute("update userdetails set user_pass=%s where username=%s", (new_p, user))
            db_connection.commit()
            return "SUCCESSFULLY CHANGED PASSWORD"
        else:
            return "<h1>PASSWORD IS NOT MATCHING</h1>"
    return render_template('change_pass.html')


@app.route('/delete_user',methods=['GET','POST'])
def delete():
    lst = []
    if request.method == 'POST':
        user = request.form.get('name')
        lst.append(user)

        my_cursor.execute("delete from userdetails where username = %s",lst)
        db_connection.commit()
        return "SUCCESSFULLY DELTED USER"
    return render_template('delete.html')


app.run(debug=True)