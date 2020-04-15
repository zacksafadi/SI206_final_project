from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import json

# create BeautifulSoup object
url = "https://www.cdc.gov/coronavirus/2019-ncov/cases-updates/cases-in-us.html"
r = requests.get(url)
data = r.text
soup = BeautifulSoup(data, "lxml")

states = soup.find_all(class_="mb-3")
request_url = "https://www.cdc.gov" + states[6].get("data-config-url")
r1 = requests.get(request_url)
info_dict = requests.get(request_url).json()
#print(info_dict)
state_list = []
for state in info_dict["data"]:
    state_dict = {}
    state_dict["Jurisdiction"] = state.get("Jurisdiction", None)
    state_dict["Cases"] = state.get("Cases Reported", None)
    state_dict["Transmission"] = state.get("Community Transmission�", None)
    state_list.append(state_dict)
print(state_list)

#print(len(states))