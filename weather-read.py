# starter for rahul to pull from weather API (had to add something to file so I could upload it to GitHub)
import requests
import json

r = requests.get("http://api.openweathermap.org/data/2.5/forecast?id=5128581&APPID=3c9071d80e11b58d16bd45c0ab95c7ad")
j=r.json()
print(j)

