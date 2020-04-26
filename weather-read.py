# starter for rahul to pull from weather API (had to add something to file so I could upload it to GitHub)
import requests
import re
import os
import csv
import json
import sqlite3

def get_jurisdiction_list(filename) :
    #Gets list of states to pull weather data for
    with open(filename) as f:
        jurisdiction_list = f.readlines()
    jurisdiction_list = [jurisdiction.strip() for jurisdiction in jurisdiction_list] 
    return jurisdiction_list


def get_jurisdictions():
    #loads in ID list for OpenWeatheMap API
    with open('city.list.json') as f:
        locations = json.load(f)
    return locations


#Test function to get weather data for a state
def get_weather_data(ids, state):
    request_url = "http://api.openweathermap.org/data/2.5/forecast?id=" + str(ids[state]) + "&APPID=3c9071d80e11b58d16bd45c0ab95c7ad&units=imperial"
    r = requests.get(request_url)
    j=r.json()
    id = ids[state]
    temp = j['list'][0]['main']['temp']
    min = j['list'][0]['main']['temp_min']
    max = j['list'][0]['main']['temp_max']
    weather = j['list'][0]['weather'][0]['main']
    return (id, state, temp, min, max, weather)


def print_weather_data(ids):
    #Prints out all states weather information from state_list 
    for location in ids:
        print(get_weather_data(ids, location))
        print()


def write_to_db(ids):
    # set up connection to the database
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/SI206_final_db.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS US_Jurisdiction_Weather (id INTEGER PRIMARY KEY, jurisdiction TEXT, temp INTEGER, min INTEGER, max INTEGER, weather TEXT)")

    for loc in ids:
        cur.execute("SELECT temp FROM US_Jurisdiction_Weather WHERE id = ? LIMIT 1", (ids[loc], ))
        try:
            id, state, temp, min, max, weather = get_weather_data(ids, loc)
            mysql = "UPDATE US_Jurisdiction_Weather SET temp=?, min=?, max=?, weather=? WHERE id==?"
            cur.execute(mysql, (temp, min, max, weather, id))
        except:
            cur.execute("INSERT INTO US_Jurisdiction_Weather (id, jurisdiction, temp, min, max, weather) VALUES (?,?,?,?,?, ?)",
            get_weather_data(ids, loc))

    conn.commit()


def main():
    jurisdictions = get_jurisdictions()
    jurisdiction_list = get_jurisdiction_list("state_list.txt")

    #creates dict for ids for locs in jurisdictions
    ids = {}
    for loc in jurisdictions:
        if loc['name'] in jurisdiction_list:
            ids[loc['name']] = loc['id']

    print_weather_data(ids)
    #write_to_db(ids)

if __name__ == "__main__":
    main()