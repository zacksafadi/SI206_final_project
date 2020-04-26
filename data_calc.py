# data calculation and database joins
import os
import csv
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
        if region[1] == "None":
            continue
        total += int(region[1])
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
    avg_cold_cases = getAvgCasesByWeather(cold_list)
    avg_warm_cases = getAvgCasesByWeather(warm_list)
    avg_hot_cases = getAvgCasesByWeather(hot_list)

    f = open("cases_data.txt", "w")
    f.write("(Average Cloud Cases," + str(avg_cloud_cases) + ")\n")
    f.write("Average Rain Cases," + str(avg_rain_cases) + ")\n")
    f.write("Average Clear Cases," + str(avg_clear_cases) + ")\n")
    f.write("Average Cold Cases (30-50)," + str(avg_cold_cases) + ")\n")
    f.write("Average Warm Cases (50-70)," + str(avg_warm_cases) + ")\n")
    f.write("Average Hot Cases (70-90)," + str(avg_hot_cases) + ")\n")
    f.close()


if __name__ == "__main__":
    main()
