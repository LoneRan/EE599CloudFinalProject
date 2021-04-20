from flask import Flask, render_template, request, redirect
import requests
import json
app = Flask(__name__)
CHECK = 0


@app.route("/")
def home():

    return render_template("index.html")

@app.route('/about')
def form():
    
    return render_template('about.html')

@app.route('/contact')
def data():
    
    return render_template('data.html')

@app.route('/login')
def login():
    
    return render_template('login.html')