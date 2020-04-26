import csv
import matplotlib
import matplotlib.pyplot as plt


def get_data(filename):
    f = open(filename, "r")
    data = f.readlines()
    f.close()
    return data


def create_graph(temps, cases):
    width = 0.5
    fig, ax = plt.subplots()
    p1 = ax.bar(temps, cases, width, color='orange')
    ax.set(xlabel='Temperature Range (F)', ylabel='Avg Number of Covid Cases',
        title='Average Number of Covid-19 Cases by Temperature Range')
    ax.grid()
    plt.show()  


def main():
    data = get_data("cases_data.txt")
    #only interested in data[3] through data[5] for this graph
    temps = ['30º-49º', '50º-69º', '70º-89º']
    cases = []
    for line in data:
        if line.find("Cloud") != -1 or line.find("Clear") != -1 or line.find("Rain") != -1:
            continue
        stats = line.split(",")
        cases.append(float(stats[1][:-2]))
    create_graph(temps, cases)

if __name__ == "__main__":
    main()