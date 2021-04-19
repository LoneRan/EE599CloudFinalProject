import json
import requests
from datetime import datetime, timedelta


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

def getYesterday(s):
    date = datetime.strptime(s, "%Y-%m-%d")
    modified_date = date + timedelta(days=1)
    yesterday = datetime.strftime(modified_date, "%Y-%m-%d") 
    return yesterday

def getSevenByState(state):
    #today = datetime.today().strftime('%Y-%m-%d')
    today = '2020-08-11'
    yesterday = getYesterday(today)
    print(today)

    StateCodeMetaData = requests.get('https://api.covidtracking.com/v2/states.json').json()['data']
    StateCode = []
    for dic in StateCodeMetaData:
        StateCode.append(dic['state_code'].lower())

    output_data = {}
    request_form = 'https://api.covidtracking.com/v2/states/{}/' + yesterday + '.json'
    print(request_form)
    for state in StateCode:
        r = requests.get(request_form.format(state)).json()
        output_data[state.upper()] = r['data']

    print(json.dumps(output_data[state],indent=4))

#TODO save to database