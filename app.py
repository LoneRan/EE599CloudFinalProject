from flask import Flask, render_template, request, redirect, url_for, Response, session
import requests
import json
from helper import guessState
import userProfile

import mysql.connector
from os import path
from covid_pred import predict_next

app = Flask(__name__)
app.secret_key = 'any random string'
CHECK = 0

######### connect to database
file_path = "./config/mysql.json"
host_id = ""
user_id = ""
password_id = ""
if(path.exists(file_path) == False):
     exit(2)

f = open("./config/mysql.json")
data = json.load(f)
host_id = data['host']
user_id = data['user']
password_id = data['pass']
db = mysql.connector.connect(
    host=host_id,
    user=user_id,
    password=password_id
)
cursor = db.cursor()
######### database connection

states_names = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
                "Connecticut","District of Columbia","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
                "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
                "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
                "Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
                "North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
                "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
                "Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]

states_abbr = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
                "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
                "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
                "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
                "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
states_names_upper = [x.upper() for x in states_names]
state_dict = dict(zip(states_names_upper, states_abbr))




@app.route("/")
def home():
    # 
    # session.pop('username', None)
    # print(session)
    return render_template("index.html",login=session)

@app.route('/about')
def form():
    
    return render_template('about.html')

@app.route('/contact')
def data():

    return render_template('result_cp.html')


@app.route('/searchState', methods=['POST','GET'])
def searchState():
    stateName = request.form['stateName']
    print(stateName)
    guessName = guessState(stateName)

    isGuess = False
    # check if we need to guess what user means
    if guessName != stateName:
        
        isGuess = True
    
    proc_name = guessName.upper()
    if proc_name not in states_abbr:
        proc_name = state_dict[proc_name]

    
    query = "SELECT * FROM coviddb.covid_trend WHERE state_name='%s'" %(proc_name)
    cursor.execute(query)

    data_raw = cursor.fetchall()
    print(data_raw)

    labels = [1,2,3,4,5,6,7]
    data_covid = []
    if len(data_raw) != 0:
        data_covid = data_raw[0][1:]
        data_covid = list(data_covid)
        print(data_covid)
    
    query_30 = "SELECT * FROM coviddb.covid_data_30 WHERE state_name='%s'" %(proc_name)
    cursor.execute(query_30)

    data_raw_30 = cursor.fetchall()
    print(data_raw_30)

    labels_30 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
    data_covid_30 = []
    if len(data_raw_30) != 0:
        data_covid_30 = data_raw_30[0][1:]
        data_covid_30 = list(data_covid_30)
        print(data_covid_30)
    covid_next = predict_next(data_covid_30)

    avg_seven = 0
    for i in data_covid:
        avg_seven = avg_seven + i/7
    #if login, check whether user has already added the state to wishlist
    #this is used to control add/delete from wishlist button
    isWish = False
    if 'username' in session:
        isWish = userProfile.checkWish(session['username'], guessName)

    return render_template('result.html', 
        stateName = stateName, guessName = guessName, isGuess = isGuess,
        labels=labels,data_covid=data_covid,
        labels_30=labels_30,data_covid_30=data_covid_30,
        covid_next = (int)(covid_next), 
        avg_seven = avg_seven,
        login=session, isWish=isWish)


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
        repeatpass = request.form['repeatpass']
        if password!=repeatpass:
            return render_template('login.html',data=6) #two password entered are not same!
        fname, lname = fullname.strip().split(' ')
        if userProfile.checkDupProfile(email): #check whether email has been used for registration
            return render_template('login.html',data=3) #email is used!
        userProfile.register(fname, lname, email, password) #update db for registration
        return render_template('login.html',data=2)
    if request.method == 'GET' and len(request.args) > 0:
        email = request.args['email']
        password = request.args['pass']
        if not userProfile.checkCredential(email, password): #login not successfully
            return render_template('login.html',data=1)
        else:    #login successfully
            session['username'] =email
            return render_template("index.html", login=session) #this email is the username, cannot be changed
    return render_template('login.html')

@app.route('/profile/<username>', methods=['POST','GET'])
def profile(username): #name is user's info
    fname = userProfile.getFirstName(username)
    userData, wishlist = userProfile.generateInfo(username)
    data = [fname,username,userData,wishlist]
    if request.method == 'POST':
        if 'Home' in request.form:
            return render_template("index.html", login=session)
        elif 'submit' in request.form:
            userProfile.updateProfile(request.form,username)
            data[0] = userProfile.getFirstName(username)
            data[2],data[3] = userProfile.generateInfo(username)
    return render_template("profile.html", data=data)

@app.route('/wishlist/<username>', methods=['POST','GET'])
def wishlist(username):
    # print(request.form)
    if 'delete' in request.form:
        userProfile.deleteWishlist(username,request.args['state'])
    elif 'add' in request.form:
        userProfile.addWishlist(username,request.args['state'])
    
    return redirect(f'/profile/{username}')
@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template("index.html", login=session)