from flask import Flask, render_template, request, redirect, url_for, Response
import requests
import json
from helper import guessState
app = Flask(__name__)
CHECK = 0


@app.route("/")
def home():
    # email = request.args['email']
    # password = request.args['pass']
    # print(email)
    # print(password)
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


@app.route('/login',methods=['POST','GET'])
def login():

    return render_template('login.html')


@app.route('/login/check',methods=['GET'])
def loginCheck():
    email = request.args['email']
    password = request.args['pass']
    print(email)
    if password == '0':
        return render_template('login.html')
    else:
        data = 1
        return render_template("index.html",data=data)

# @app.route('/profile')