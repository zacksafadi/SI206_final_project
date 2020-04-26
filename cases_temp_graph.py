import csv
import matplotlib
import matplotlib.pyplot as plt

f = open("cases_data.txt", "r")
data = f.readlines()
f.close()
 #only interested in data[3] through data[5] for this graph
temps = []
cases = []
for line in data:
    if line.find("Cloud") != -1 or line.find("Clear") != -1 or line.find("Rain") != -1:
        continue
    stats = line.split(",")
    temps.append(stats[0][1:])
    cases.append(float(stats[1][:-2]))



fig = plt.figure(figsize=(10,5))
