from bs4 import BeautifulSoup
from datetime import datetime
import requests
import re
import os
import csv
import json
import sqlite3

# create BeautifulSoup object
url = "https://www.cdc.gov/coronavirus/2019-ncov/cases-updates/cases-in-us.html"
r = requests.get(url)
data = r.text
soup = BeautifulSoup(data, "lxml")

states = soup.find_all(class_="mb-3")
request_url = "https://www.cdc.gov/coronavirus/2019-ncov/json/us-cases-map-data.json"
r1 = requests.get(request_url)
info_dict = requests.get(request_url).json()
#print(info_dict)
state_list = []
for state in info_dict:
    state_dict = {}
    state_dict["Jurisdiction"] = state.get("Jurisdiction", None)
    state_dict["Cases"] = state.get("Cases Reported", None)
    transmission = state.get("Community Transmission", None)
    if transmission == None:
        state_dict["Transmission"] = transmission
    elif transmission.find("Yes") == -1:
        state_dict["Transmission"] = transmission
    else:
        trans = transmission.split(", ")
        state_dict["Transmission"] = trans[1]
    state_list.append(state_dict)


#Records all jurisdictions into text file
file = open('state_list.txt', 'w') 
for state in state_list:
    file.write(state['Jurisdiction']+'\n')
file.close() 




# set up connection to the database
path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path+'/SI206_final_db.db')
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS US_Covid_19_Cases")
cur.execute("DROP TABLE IF EXISTS US_Covid_19_Transmission")
cur.execute("CREATE TABLE US_Covid_19_Cases (id INTEGER PRIMARY KEY, jurisdiction TEXT, cases TEXT, timestamp TEXT)")
cur.execute("CREATE TABLE US_Covid_19_Transmission (id INTEGER PRIMARY KEY, jurisdiction TEXT, transmission TEXT, timestamp TEXT)")
for i in (range(len(state_list) - 1)):
    cur.execute("INSERT INTO US_Covid_19_Cases (id, jurisdiction, cases, timestamp) VALUES (?,?,?,?)",(i,state_list[i]["Jurisdiction"],state_list[i]["Cases"],datetime.now()))
    cur.execute("INSERT INTO US_Covid_19_Transmission (id, jurisdiction, transmission, timestamp) VALUES (?,?,?,?)",(i,state_list[i]["Jurisdiction"],state_list[i]["Transmission"],datetime.now()))
conn.commit()

