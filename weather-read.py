# starter for rahul to pull from weather API (had to add something to file so I could upload it to GitHub)
import requests
import re
import os
import csv
import json
import sqlite3

#Gets list of states to pull weather data for
with open("state_list.txt") as f:
    state_list = f.readlines()
state_list = [state.strip() for state in state_list] 

#loads in ID list for OpenWeatheMap API
with open('city.list.json') as f:
  locations = json.load(f)

#creates dict for ids for states in state_list
location_ids = {}
for loc in locations:
    if loc['name'] in state_list:
        location_ids[loc['name']] = loc['id']


#Test function to get weather data for a state
def get_weather_data(state):
    request_url = "http://api.openweathermap.org/data/2.5/forecast?id=" + str(location_ids[state]) + "&APPID=3c9071d80e11b58d16bd45c0ab95c7ad&units=imperial"
    r = requests.get(request_url)
    j=r.json()
    id = location_ids[state]
    temp = j['list'][0]['main']['temp']
    min = j['list'][0]['main']['temp_min']
    max = j['list'][0]['main']['temp_max']
    weather = j['list'][0]['weather'][0]['main']
    return (id, state, temp, min, max, weather)



#Prints out all states weather information from state_list 
'''for location in location_ids:
    get_weather_data(location)
    print()'''

# set up connection to the database
path = os.path.dirname(os.path.abspath(__file__))

conn = sqlite3.connect(path+'/SI206_final_db.db')

cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS US_Jurisdiction_Weather (id INTEGER PRIMARY KEY, jurisdiction TEXT, temp INTEGER, min INTEGER, max INTEGER, weather TEXT)")

for location in location_ids:
    try:
        id, state, temp, min, max, weather = get_weather_data(location)
        mysql = "UPDATE US_Jurisdiction_Weather SET temp="+str(temp)+", min="+str(min)+", max="+str(max)+", weather="+weather+" WHERE id="+str(location_ids[location])
        cur.execute(mysql)
    except:
        cur.execute("INSERT INTO US_Jurisdiction_Weather (id, jurisdiction, temp, min, max, weather) VALUES (?,?,?,?,?, ?)",
        get_weather_data(location))

conn.commit()