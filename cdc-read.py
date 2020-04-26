from bs4 import BeautifulSoup
from datetime import datetime
import requests
import re
import os
import csv
import json
import sqlite3

def readFromUrl(url):
    info_list = requests.get(url).json()
    state_list = []
    trans_list = []
    for i in range(4):
        trans_list.append("N/A")
        trans_list.append("Undetermined")
        trans_list.append("defined area(s)")
        trans_list.append("widepsread")
    for state in info_list:
        state_dict = {}
        state_dict["Jurisdiction"] = state.get("Jurisdiction", None)
        state_dict["Cases"] = state.get("Cases Reported", None)
        if state.get("Community Transmission", None) == "N/A":
            state_dict["trans_id"] = 0
        elif state.get("Community Transmission", None) == "Undetermined":
            state_dict["trans_id"] = 1
        elif state.get("Community Transmission", None) == "Yes, defined area(s)":
            state_dict["trans_id"] = 2
        else:
            state_dict["trans_id"] = 3
        state_list.append(state_dict)
    return trans_list, state_list
    
def writeStatesToFile(filename, state_list):
    file = open(filename, 'w') 
    for state in state_list:
        file.write(state['Jurisdiction']+'\n')
    file.close()

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def updateCasesTable(data, cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS US_Covid_19_Cases (id INTEGER PRIMARY KEY, jurisdiction TEXT, cases TEXT, transmission_id INTEGER)")
    for i in (range(len(data) - 1)):
        try:
            # if already there, update the number of cases
            cur.execute("UPDATE US_Covid_19_Cases SET cases = ?, transmission_id = ? WHERE jurisdiction = ?",(data[i]["Cases"], data[i]["trans_id"], data[i]["Jurisdiction"]))
        except:
            # not there, so insert it
            cur.execute("INSERT INTO US_Covid_19_Cases (id, jurisdiction, cases, transmission_id) VALUES (?,?,?,?)",(i,data[i]["Jurisdiction"],data[i]["Cases"],data[i]["trans_id"]))
    conn.commit()

def updateTransmissionTable(data, cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS US_Covid_19_Transmission (id INTEGER PRIMARY KEY, transmission TEXT)")
    cur.execute("SELECT transmission FROM US_Covid_19_Transmission WHERE id = 1 LIMIT 1")
    if cur.fetchone() == None:
        for j in range(4):
            cur.execute("INSERT INTO US_Covid_19_Transmission (id, transmission) VALUES (?,?)",(j, data[j]))
        conn.commit()

def main():
    trans_data, state_data = readFromUrl("https://www.cdc.gov/coronavirus/2019-ncov/json/us-cases-map-data.json")
    writeStatesToFile('state_list.txt', state_data)
    cur, conn = setUpDatabase('SI206_final_db.db')
    updateTransmissionTable(trans_data, cur, conn)
    updateCasesTable(state_data, cur, conn)

if __name__ == "__main__":
    main()