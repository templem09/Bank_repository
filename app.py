from flask import Flask, render_template, request
import sqlite3
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD']= True

@app.route("/")
def home():
    return render_template('index.html')