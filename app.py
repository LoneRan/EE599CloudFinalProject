from flask import Flask, render_template, request, redirect, url_for, Response, session
import requests, urllib.request
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

states_policy = ["https://www.alabamapublichealth.gov/covid19/index.html", "http://dhss.alaska.gov/dph/Epi/id/Pages/COVID-19/default.aspx", "https://www.azdhs.gov/covid19/index.php",
                 "https://www.healthy.arkansas.gov/programs-services/topics/novel-coronavirus", "https://www.cdph.ca.gov/Programs/CID/DCDC/Pages/Immunization/ncov2019.aspx",
                 "https://covid19.colorado.gov/", "https://portal.ct.gov/Coronavirus", "https://dhss.delaware.gov/dhss/dph/index.html", "https://floridahealthcovid19.gov/",
                 "https://gov.georgia.gov/executive-action/executive-orders/2021-executive-orders", "https://hawaiicovid19.com/", "https://coronavirus.idaho.gov/governors-actions/",
                 "http://www.dph.illinois.gov/", "https://www.coronavirus.in.gov/", "https://coronavirus.iowa.gov/?utm_medium=email&utm_source=govdelivery", "https://covid.ks.gov/",
                 "https://govstatus.egov.com/kycovid19", "https://ldh.la.gov/coronavirus/", "https://www.maine.gov/dhhs/mecdc/infectious-disease/epi/airborne/coronavirus/index.shtml",
                 "https://coronavirus.maryland.gov/", "https://www.mass.gov/resource/information-on-the-outbreak-of-coronavirus-disease-2019-covid-19", 
                 "https://www.michigan.gov/coronavirus", "https://www.health.state.mn.us/diseases/coronavirus/index.html", "https://msdh.ms.gov/msdhsite/_static/14,0,420.html", 
                 "https://health.mo.gov/living/healthcondiseases/communicable/novel-coronavirus/", "https://dphhs.mt.gov/publichealth/cdepi/diseases/coronavirusmt", 
                 "https://dhhs.ne.gov/Pages/default.aspx", "https://nvhealthresponse.nv.gov/", "https://www.covid19.nh.gov/", "https://covid19.nj.gov/", "https://cv.nmhealth.org/", 
                 "https://www.governor.ny.gov/news", "https://covid19.ncdhhs.gov/", "https://www.health.nd.gov/diseases-conditions/coronavirus", "https://odh.ohio.gov/wps/portal/gov/odh/home", 
                 "https://oklahoma.gov/covid19.html", "https://govstatus.egov.com/OR-OHA-COVID-19", "https://www.health.pa.gov/topics/disease/coronavirus/Pages/Coronavirus.aspx", 
                 "https://health.ri.gov/diseases/respiratory/?parm=163", "https://scdhec.gov/covid19", "https://doh.sd.gov/COVID/", "https://www.tn.gov/health/cedep/ncov.html", 
                 "https://www.dshs.texas.gov/coronavirus/", "https://coronavirus.utah.gov/", "https://www.healthvermont.gov/covid-19", "https://www.vdh.virginia.gov/coronavirus/",
                 "https://www.doh.wa.gov/Emergencies/COVID19", "https://dhhr.wv.gov/COVID-19/Pages/default.aspx", "https://www.dhs.wisconsin.gov/outbreaks/index.htm",
                 "https://health.wyo.gov/publichealth/infectious-disease-epidemiology-unit/disease/novel-coronavirus/"]


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
state_dict_reverse = dict(zip(states_abbr, states_names))



@app.route("/")
def home():
    # 
    # session.pop('username', None)
    # print(session)
    q = "SELECT state_name, average FROM coviddb.covid_trend ORDER BY average DESC LIMIT 5"
    cursor.execute(q)
    data_raw = cursor.fetchall()
    # print(data_raw[0][0])
    return render_template("index.html",login=session, top5 = data_raw)

@app.route('/Weather', methods = ['POST', 'GET'])
def weather():
    if request.method == 'POST':
        state_code = request.form['state_code']
    else:
        state_code = 'CA'
    
    api = "03e8fdf7e4bd0c38e8c16b18799f055e"

    source = urlib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q =' + state_code + '&appid =' + api).read()

    list_of_data = json.loads(source)

    data = {
        "country_code": str(list_of_data['sys']['country']),
        "coordinate": str(list_of_data['coord']['lon']) + ' ' + str(list_of_data['coord']['lat']),
        "temp": str(list_of_data['main']['temp']) + 'k',
        "pressure": str(list_of_data['main']['pressure']),
        "humidity": str(list_of_data['main']['humidity']),
    }
    print(data)
    return render_template('weather.html', data = data)

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

    # For weather API usage
    weather_name = (str)(state_dict_reverse[proc_name])
    print(weather_name)

    query = "SELECT * FROM coviddb.covid_trend WHERE state_name='%s'" %(proc_name)
    cursor.execute(query)

    data_raw = cursor.fetchall()
    print(data_raw)

    labels = [1,2,3,4,5,6,7]
    data_covid = []
    if len(data_raw) != 0:
        data_covid = data_raw[0][1:8]
        data_covid = list(data_covid)
        print(data_covid)
    data_covid.reverse()
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
    data_covid_30.reverse()
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
        weather_name = weather_name,
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