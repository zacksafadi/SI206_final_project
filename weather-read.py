# starter for rahul to pull from weather API (had to add something to file so I could upload it to GitHub)
import requests
import json

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
    print(state, "Data")
    print("Temp:", j['list'][0]['main']['temp'])
    print("Min:", j['list'][0]['main']['temp_min'])
    print("Max:", j['list'][0]['main']['temp_max'])
    print("Weather:", j['list'][0]['weather'][0]['main'])


#Prints out all states weather information from state_list 
for location in location_ids:
    get_weather_data(location)
    print()

