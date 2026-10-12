from flask import Flask, render_template, request
import sqlite3
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD']= True
invalid = 'valid'
@app.route("/")
def start():
   return render_template('login.html')


@app.route("/home.html")
def home():
   return render_template('home.html')


@app.route("/", methods = ['GET','POST'])
def login():
   global invalid
   if request.method == 'POST':
       employee_name = request.form.get('employee_name')
       db = sqlite3.connect("bank.db")
       cursor = db.cursor()
       results_display= set()
       try:
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
       except:
           return render_template ('login.html', invalid = 'Username or password incorrect.')
       if len(results_display) == 1:
           return render_template ('home.html')
       else:
           return render_template ('login.html', invalid = 'Username or password incorrect.')


@app.route('/details.html')
def details():
   db = sqlite3.connect("bank.db")
   cursor = db.cursor()
   results_display= []
   sql = (f"""SELECT person_id, name, birthday
           from details
           """)
   cursor.execute(sql)
   details = cursor.fetchall()
   results_display.append(details)
   return render_template('details.html', customers=results_display[0])


@app.route('/customer.html/<int:customer_id>')
def customer(customer_id):
   db = sqlite3.connect("bank.db")
   cursor = db.cursor()
   results_display= []
   sql = (f"""SELECT person_id, name, birthday, email, phone_number
               from details
               WHERE person_id = {customer_id}
               """)
   cursor.execute(sql)
   details = cursor.fetchall()
   results_display.append(details)
   return render_template('customer.html', customer=results_display[0])

