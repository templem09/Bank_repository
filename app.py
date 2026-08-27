from flask import Flask, render_template, request
import sqlite3
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD']= True

@app.route("/")
def home():
    return render_template('login.html')


@app.route("/", methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        employee_name = request.form.get('employee_name')
        db = sqlite3.connect("bank.db")
        cursor = db.cursor()
        results_display= set()
        sql = (f"""SELECT employee_id
                from log_in
                WHERE employee = '{employee_name}'
                """)
        cursor.execute(sql)
        employee_id = cursor.fetchall()
        results_display.add(employee_id[0][0])
        password = request.form.get('password')
        sql = (f"""SELECT employee_id
                        from log_in
                        WHERE password = '{password}'
                        """)
        cursor.execute(sql)
        password = cursor.fetchall()
        results_display.add(password[0][0])
        if len(results_display) == 1:
            return render_template ('index.html')
        else:
            invalid = 'Username or password incorrect.'
            return render_template ('login.html', invalid = invalid)