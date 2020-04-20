import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import sqlite3

connection = sqlite3.connect('caseupdates.sqlite')
cursor = connection.cursor()
cursor.execute("""SELECT COUNTY, CASES
FROM CASES ORDER BY SET_ID ASC""");

counties = []
index = None
counts = []
while True:
    row = cursor.fetchone()
    if row is None:
        break
    else:
        (county, cases) = row
    if county not in counties:
        counties.append(county)
        counts.append([])
        index = len(counties) - 1
    else:
        for i in range(len(counties)):
            if county == counties[i]:
                index = i
                break
    counts[index].append(cases)

# based on https://stackoverflow.com/questions/4534480/get-legend-as-a-separate-picture-in-matplotlib
figData = pylab.figure(figsize=(8.5, 11))
ax = pylab.gca()

for i in range(len(counts)):
    x = []
    y = []
    for j in range(len(counts[i])):
        x.append(j)
        y.append(counts[i][j])
    pylab.plot(x, y, label=counties[i])

figLegend = pylab.figure(figsize=(8.5, 11))
pylab.figlegend(*ax.get_legend_handles_labels(), loc='upper left', ncol=5)
figData.show()
figLegend.show()
