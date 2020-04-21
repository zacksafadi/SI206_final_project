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
trans_list = []
for i in range(4):
    trans_list.append("N/A")
    trans_list.append("Undetermined")
    trans_list.append("defined area(s)")
    trans_list.append("widepsread")
for state in info_dict:
    state_dict = {}
    state_dict["Jurisdiction"] = state.get("Jurisdiction", None)
    state_dict["Cases"] = state.get("Cases Reported", None)
    '''transmission = state.get("Community Transmission", None)
    if transmission == None:
        state_dict["Transmission"] = transmission
    elif transmission.find("Yes") == -1:
        state_dict["Transmission"] = transmission
    else:
        trans = transmission.split(", ")
        state_dict["Transmission"] = trans[1]'''
    
    if state.get("Community Transmission", None) == "N/A":
        state_dict["trans_id"] = 0
    elif state.get("Community Transmission", None) == "Undetermined":
        state_dict["trans_id"] = 1
    elif state.get("Community Transmission", None) == "Yes, defined area(s)":
        state_dict["trans_id"] = 2
    else:
        state_dict["trans_id"] = 3
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
cur.execute("CREATE TABLE IF NOT EXISTS US_Covid_19_Cases (id INTEGER PRIMARY KEY, jurisdiction TEXT, cases TEXT, transmission_id INTEGER)")
cur.execute("CREATE TABLE IF NOT EXISTS US_Covid_19_Transmission (id INTEGER PRIMARY KEY, transmission TEXT)")
for i in (range(len(state_list) - 1)):
    cur.execute("SELECT transmission FROM US_Covid_19_Transmission WHERE id = 1 LIMIT 1")
    if cur.fetchone() == None:
        for j in range(4):
            cur.execute("INSERT INTO US_Covid_19_Transmission (id, transmission) VALUES (?,?)",(j, trans_list[j]))

    cur.execute("SELECT cases FROM US_Covid_19_Cases WHERE jurisdiction = ? LIMIT 1",(state_list[i]["Jurisdiction"], ))
    try:
        # if already there, update the number of cases
        cur.execute("UPDATE US_Covid_19_Cases SET cases = ?, transmission_id = ? WHERE jurisdiction = ?",(state_list[i]["Cases"], state_list[i]["trans_id"], state_list[i]["Jurisdiction"]))
    except:
        # not there, so insert it
        cur.execute("INSERT INTO US_Covid_19_Cases (id, jurisdiction, cases, transmission_id) VALUES (?,?,?,?)",(i,state_list[i]["Jurisdiction"],state_list[i]["Cases"],state_list[i]["trans_id"]))
conn.commit()