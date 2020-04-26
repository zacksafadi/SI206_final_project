# data calculation and database joins
import os
import sqlite3

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def getCasesByWeather(cur, conn, weather):
    cur.execute("SELECT US_Jurisdiction_Weather.jurisdiction, US_Covid_19_Cases.cases, US_Jurisdiction_Weather.temp, US_Jurisdiction_Weather.weather FROM US_Jurisdiction_Weather JOIN US_Covid_19_Cases ON US_Jurisdiction_Weather.jurisdiction = US_Covid_19_Cases.jurisdiction WHERE US_Jurisdiction_Weather.weather = ?",(weather, ))
    return cur.fetchall()

def main():
    cur, conn = setUpDatabase('SI206_final_db.db')
    print(getCasesByWeather(cur, conn, "Clouds"))

if __name__ == "__main__":
    main()
