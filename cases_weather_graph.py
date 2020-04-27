import csv
import matplotlib
import matplotlib.pyplot as plt


def get_data(filename):
    f = open(filename, "r")
    data = f.readlines()
    f.close()
    return data


def create_graph(weather, cases):
    fig, ax = plt.subplots()
    p1 = ax.bar(weather, cases, 0.5, color='orange')
    ax.set(xlabel='Weather Patterns', ylabel='Avg Number of Covid Cases',
        title='Average Number of Covid-19 Cases by Weather')
    ax.grid()

    plt.show()


def main():
    data = get_data("cases_data.txt")

    weather = ['Clouds', 'Rain', 'Clear']
    cases = []
    for line in data:
        if line.find("Cold") != -1 or line.find("Warm") != -1 or line.find("Hot") != -1:
            continue
        stats = line.split(",")
        cases.append(float(stats[1][:-2]))

    create_graph(weather, cases)

    print(cases)

if __name__ == "__main__":
    main()