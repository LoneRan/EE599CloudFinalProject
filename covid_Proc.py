import json
import requests
from datetime import datetime, timedelta
import pandas as pd
import mysql.connector
from os import path
from sqlalchemy import create_engine
# StateCodeMetaData = requests.get('https://api.covidtracking.com/v2/states.json').json()['data']
# StateCode = []
# for dic in StateCodeMetaData:
# 	StateCode.append(dic['state_code'].lower())

# output_data = {}

# for state in StateCode:
# 	r = requests.get('https://api.covidtracking.com/v2/states/{}/2020-08-01.json'.format(state)).json()
# 	output_data[state.upper()] = r['data']

# print(json.dumps(output_data['CA'],indent=4))
#print(output_data['CA'])
#def getSevenByState(state):
    #first get today's date


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
# cursor = db.cursor()
# cursor.execute("show databases")
# print(cursor.fetchall())

engine = create_engine("mysql+pymysql://admin:ee599final@ee599db.cs9tlndyzuyd.us-west-2.rds.amazonaws.com:3306/coviddb",pool_size =1)
engine.connect()


def getYesterday(s):
    date = datetime.strptime(s, "%Y-%m-%d")
    modified_date = date - timedelta(days=1)
    yesterday = datetime.strftime(modified_date, "%Y-%m-%d") 
    return yesterday

def getTodayCases(today):
    #today = datetime.today().strftime('%Y-%m-%d')
    # today = '2020-08-10'
    # yesterday = getYesterday(today)
    # print(yesterday)

    StateCodeMetaData = requests.get('https://api.covidtracking.com/v2/states.json').json()['data']
    StateCode = []
    for dic in StateCodeMetaData:
        StateCode.append(dic['state_code'].lower())
    output_data = {}
    request_form = 'https://api.covidtracking.com/v2/states/{}/' + today + '.json'
    print(request_form)
    for state in StateCode:
        # print(request_form.format(state))
        r = requests.get(request_form.format(state)).json()
        # print(r)
        if('error' in r):
            output_data[state.upper()]= 0
        else:
            output_data[state.upper()] = r['data']
    # print(output_data)
    res = []
    for state in StateCode:
        if output_data[state.upper()]== 0:
            res.append(0)
        else:
            res.append(output_data[state.upper()]['cases']['total']['calculated']['change_from_prior_day'])
    # print(json.dumps(output_data[st],indent=4))
    ret = pd.DataFrame({today:res})
    return ret

#TODO save to database

# print(getTodayCases('2020-08-10'))

StateCodeMetaData = requests.get('https://api.covidtracking.com/v2/states.json').json()['data']
StateCode = []
for dic in StateCodeMetaData:
    StateCode.append(dic['state_code'].lower())
# sort(StateCode)
# column_names = ['state_name','7','6','5','4','3','2','1']
# df = pd.DataFrame(columns=column_names)
state_names = []
for state in StateCode:
    state_names.append(state.upper())
df = pd.DataFrame({'state_name':state_names})


today = '2021-02-11'
for i in range(7):
    today = getYesterday(today)
    # df.join(getTodayCases(today))
    df = pd.concat([df, getTodayCases(today)], axis=1)
print(df)

average = []
for i in range(56):
    temp = 0
    for j in range(1,8):
        temp = temp + df.iloc[i,j]
    temp = (int)(temp/7)
    average.append(temp)

avg = pd.DataFrame({'average': average})
df = pd.concat([df, avg], axis=1)
print(df)
df.to_sql('covid_trend',con=engine,if_exists='replace',index=False)
engine.dispose()
# print(getTodayCases('2021-02-11'))



df_pred = pd.DataFrame({'state_name':state_names})
def saveThirtyDays():
    today = '2021-02-11'
    for i in range(30):
        today = getYesterday(today)
        # df.join(getTodayCases(today))
        df_pred = pd.concat([df_pred, getTodayCases(today)], axis=1)
        print(df_pred)
    print(df_pred)

    df_pred.to_sql('covid_data_30',con=engine,if_exists='replace',index=False)
    engine.dispose()
