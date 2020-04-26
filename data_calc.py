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

def getCasesbyTemp(cur, conn, temp_lower, temp_upper):
    cur.execute("SELECT US_Jurisdiction_Weather.jurisdiction, US_Covid_19_Cases.cases, US_Jurisdiction_Weather.temp, US_Jurisdiction_Weather.weather FROM US_Jurisdiction_Weather JOIN US_Covid_19_Cases ON US_Jurisdiction_Weather.jurisdiction = US_Covid_19_Cases.jurisdiction WHERE US_Jurisdiction_Weather.temp >= ? AND US_Jurisdiction_Weather.temp < ?",(temp_lower, temp_upper,))
    return cur.fetchall()

def getAvgCasesByWeather(weather_list):
    total = 0
    for region in weather_list:
        total += region[1]
    return total / len(weather_list)

def main():
    cur, conn = setUpDatabase('SI206_final_db.db')

    cloud_list = getCasesByWeather(cur, conn, "Clouds")
    rain_list = getCasesByWeather(cur, conn, "Rain")
    clear_list = getCasesByWeather(cur, conn, "Clear")
    avg_cloud_cases = getAvgCasesByWeather(cloud_list)
    avg_rain_cases = getAvgCasesByWeather(rain_list)
    avg_clear_cases = getAvgCasesByWeather(clear_list)

    cold_list = getCasesbyTemp(cur, conn, 30, 50)
    warm_list = getCasesbyTemp(cur, conn, 50, 70)
    hot_list = getCasesbyTemp(cur, conn, 70, 90)


if __name__ == "__main__":
    main()
