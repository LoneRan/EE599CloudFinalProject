
from fuzzywuzzy import fuzz

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

def isValidState(state):
    print(len(states_names))
    print(len(states_abbr))
    if state in states_names or state in states_abbr:
        print("Input state is valid")
        return True
    print("Input state is invalid")
    return False

def guessState(state):
    if isValidState(state):
        return state
    
    ratio = 0
    res = ""
    for item in states_names:
        temp_ratio = fuzz.ratio(state,item)
        if temp_ratio > ratio:
            ratio = temp_ratio
            res = item
    return res

