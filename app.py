from flask import Flask, render_template, request, redirect
import requests
import json
from helper import guessState
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


@app.route('/searchState', methods=['POST'])
def searchState():
    stateName = request.form['stateName']
    print(stateName)
    guessName = guessState(stateName)
    isGuess = False
    if guessName != stateName:
        
        isGuess = True
    
    return render_template('result.html', stateName = stateName, guessName = guessName, isGuess = isGuess)


@app.route('/login')
def login():
    
    return render_template('login.html')
