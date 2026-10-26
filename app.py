from flask import Flask, render_template, request
import sqlite3
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD']= True
invalid = 'valid'
@app.route("/")
def start():
  """
  This function is the starting point of the application. It returns the login page."""
  return render_template('login.html')

@app.route("/home.html")
def home():
  """
  This function returns the home page."""
  return render_template('home.html')

@app.route("/", methods = ['GET','POST'])
def login():
 """ This function handles the login process. It checks the provided employee name and password against the database.
 If the login is correct it returns the home page, otherwise it returns the login page saying username or password incorrect."""
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

@app.route('/details.html', methods = ['GET','POST'])
def details():
 """This function returns the details page with a list of all customers in the database."""
 db = sqlite3.connect("bank.db")
 cursor = db.cursor()
 results_display= []
 if request.method == 'POST':
    search = request.form.get('search')
    sql = (f"""SELECT person_id, name, birthday
            from details
            WHERE name LIKE '%{search}%'
            """)
    cursor.execute(sql)
    details = cursor.fetchall()
    results_display.append(details)
    return render_template('details.html', customers=results_display[0])
 else:
    sql = (f"""SELECT person_id, name, birthday
            from details
            """)
    cursor.execute(sql)
    details = cursor.fetchall()
    results_display.append(details)
    return render_template('details.html', customers=results_display[0])

@app.route('/customer.html/<int:customer_id>/<int:bridge_id>/<bridge_table>')
def customer(customer_id, bridge_id, bridge_table):
  """This function returns the customer page with the details of a specific customer. 
  If it is coming from the details page it will simplt display the details of the customer clicked on.
  If it is coming from the account or loan page it will go thtough the bridge table to find the customer(s) associated with the account or loan clicked on and display their details."""
  db = sqlite3.connect("bank.db")
  cursor = db.cursor()
  if bridge_table == 'account' or bridge_table == 'loan':
    db = sqlite3.connect("bank.db")
    cursor = db.cursor()
    sql = (f"""SELECT person_id
              from person_{bridge_table}
              WHERE {bridge_table}_id = {bridge_id}
              """)
    cursor.execute(sql)
    customer_ids = cursor.fetchall()
  else:
    customer_ids = [(customer_id,)]
  results_display= []
  for i in customer_ids:
    sql = (f"""SELECT *
                from details
                WHERE person_id = {i[0]}
                """)
    cursor.execute(sql)
    details = cursor.fetchall()
    results_display.append(details)
  list_length = str(len(results_display))
  return render_template('customer.html', customer=results_display, list_length=list_length)

@app.route('/accounts.html', methods = ['GET','POST'])
def accounts():
 """This function returns the accounts page with a list of all accounts in the database."""
 db = sqlite3.connect("bank.db")
 cursor = db.cursor()
 results_display= []
 if request.method == 'POST':
    search = request.form.get('search')
    sql = (f"""SELECT account_id, account_name
            from account
            WHERE account_name LIKE '%{search}%'
            """)
    cursor.execute(sql)
    accounts = cursor.fetchall()
    results_display.append(accounts)
    return render_template('accounts.html', accounts=results_display[0])
 else:
    sql = (f"""SELECT account_id, account_name
            from account
            """)
    cursor.execute(sql)
    accounts = cursor.fetchall()
    results_display.append(accounts)
    return render_template('accounts.html', accounts=results_display[0])

@app.route('/account_info.html/<int:account_id>/<int:customer_id>/<customer>')
def account_info(account_id, customer_id, customer):
  """This function returns the account information page with the details of a specific account.
  If it is coming from the accounts page it will simplt display the details of the account clicked on.
  If it is coming from the customer page it will go thtough the bridge table to find the account(s) associated with the customer clicked on and display their details."""
  db = sqlite3.connect("bank.db")
  cursor = db.cursor()
  account_display= []
  if customer == 'valid':
    sql = (f"""SELECT account_id
              from person_account
              WHERE person_id = {customer_id}
              """)
    cursor.execute(sql)
    account_ids = cursor.fetchall()
  else:
    account_ids = [(account_id,)]
  for i in account_ids:
    sql = (f"""SELECT account_id, account_name, balance
              from account
              WHERE account_id = {i[0]}
              """)
    cursor.execute(sql)
    details = cursor.fetchall()
    account_display.append(details)
    sql2 = (f"""SELECT account_type_id
                from account
                WHERE account_id = {i[0]}
                """)
    cursor.execute(sql2)
    account_type = cursor.fetchall()
    sql = (f"""SELECT *
                from account_type
                WHERE account_type_id = {account_type[0][0]}
                """)
    cursor.execute(sql)
    details = cursor.fetchall()
    account_display.append(details)
  list_length = str(len(account_display))
  run = str(len(account_display))
  run = int(run)
  return render_template('account_info.html', account=account_display, list_length=list_length, run = run)

@app.route('/loans.html', methods = ['GET','POST'])
def loans():
 """This function returns the loans page with a list of all loans in the database."""
 db = sqlite3.connect("bank.db")
 cursor = db.cursor()
 results_display= []
 if request.method == 'POST':
    search = request.form.get('search')
    sql = (f"""SELECT loan_id, loan_reason
            from loans
            WHERE loan_reason LIKE '%{search}%'
            """)
    cursor.execute(sql)
    loans = cursor.fetchall()
    results_display.append(loans)
    return render_template('loans.html', loans=results_display[0])
 else:
  sql = (f"""SELECT loan_id, loan_reason
          from loans
          """)
  cursor.execute(sql)
  loans = cursor.fetchall()
  results_display.append(loans)
  return render_template('loans.html', loans=results_display[0])

@app.route('/loan_info.html/<int:loan_id>/<int:customer_id>/<customer>')
def loan_info(loan_id, customer_id, customer):
  """This function returns the loan information page with the details of a specific loan.
  If it is coming from the loans page it will simplt display the details of the loan clicked on.
  If it is coming from the customer page it will go thtough the bridge table to find the loan(s) associated with the customer clicked on and display their details."""
  db = sqlite3.connect("bank.db")
  cursor = db.cursor()
  loan_display= []
  if customer == 'valid':
    sql = (f"""SELECT loan_id
            from person_loan
            WHERE person_id = {customer_id}
            """)
    cursor.execute(sql)
    loan_ids = cursor.fetchall()
  else:
    loan_ids = [(loan_id,)]
  for i in loan_ids:
    sql = (f"""SELECT *
                from loans
                WHERE loan_id = {i[0]}
                """)
    cursor.execute(sql)
    details = cursor.fetchall()
    loan_display.append(details)
  list_length = str(len(loan_display))
  run = str(len(loan_display))
  run = int(run)
  return render_template('loan_info.html', loan=loan_display, list_length=list_length, run=run)
