from flask import Flask, render_template, request, redirect, url_for, Response
import requests
import json
from helper import guessState
import userProfile
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


@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        if 'Home' in request.form:
            return redirect("/")
        if 'reset' in request.form:
            data = 0
            username = request.form['username']
            password = request.form['password']
            data =  5 if userProfile.checkDupProfile(username) else 4
            if data == 5:
                userProfile.updatePassword(username,password)
            return render_template('login.html', data=data)
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['pass']
        fname, lname = fullname.strip().split(' ')
        if userProfile.checkDupProfile(email): #check whether email has been used for registration
            return render_template('login.html',data=3)
        userProfile.register(fname, lname, email, password) #update db for registration
        return render_template('login.html',data=2)
        # print(request.form)
    return render_template('login.html')

#check login condition
@app.route('/login/check',methods=['GET'])
def loginCheck():
    email = request.args['email']
    password = request.args['pass']
    if not userProfile.checkCredential(email, password): #login not successfully
        return render_template('login.html',data=1)
    else:    #login successfully
        return render_template("index.html",data=email) #this email is the username, cannot be changed

@app.route('/profile/<username>', methods=['POST','GET'])
def profile(username): #name is user's info
    fname = userProfile.getFirstName(username)
    userData = userProfile.generateInfo(username)
    data = [fname,username,userData]
    if request.method == 'POST':
        if 'Home' in request.form:
            return render_template("index.html",data=username)
        elif 'submit' in request.form:
            userProfile.updateProfile(request.form,username)
            data[0] = userProfile.getFirstName(username)
            data[2] = userProfile.generateInfo(username)
            data.append(1)
            return render_template("profile.html", data=data)
            # query = 'update profiles  '
        elif 'cancel' in request.form:
            return render_template("profile.html", data=data)
    return render_template("profile.html", data=data)