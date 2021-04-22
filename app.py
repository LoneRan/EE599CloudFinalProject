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
    
    labels = [1,2,3,4,5,6,7]
    data = [243,465,878,787,766,988,890]

    return render_template('result.html', 
        stateName = stateName, guessName = guessName, isGuess = isGuess,labels=labels,data=data)


@app.route('/login',methods=['POST','GET'])
def login():

    return render_template('login.html')


@app.route('/login/check',methods=['GET'])
def loginCheck():
    email = request.args['email']
    password = request.args['pass']
    # print(email)
    if password == '0': #login not successfully
        return render_template('login.html',data=1)
    else:    #login successfully
        return render_template("index.html",data=email)

@app.route('/profile/<name>', methods=['POST','GET'])
def profile(name): #name is user's info
    prefix = name.split('@')[0]
    data = [prefix,name]
    if request.method == 'POST':
        return render_template("index.html",data=name)
    return render_template("profile.html", data=data)