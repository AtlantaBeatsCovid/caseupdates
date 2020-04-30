from datetime import datetime

import matplotlib.pyplot as plt
import sqlite3

connection = sqlite3.connect('caseupdates.sqlite')
cursor = connection.cursor()
cursor.execute("""SELECT
       COUNTY,
       CASES,
       CASE
           WHEN COUNTY IN (
               SELECT DISTINCT(COUNTY)
               FROM CASES ORDER BY CASES DESC
               LIMIT 10
               ) THEN 1
           ELSE 0
           END
        AS IMPORTANT
FROM CASES
WHERE UPPER(COUNTY)!='UNKNOWN'
ORDER BY SET_ID ASC""")

counties = []
important_counties = []
index = None
counts = []
while True:
    row = cursor.fetchone()
    if row is None:
        break
    else:
        (county, cases, important) = row
    if county not in counties:
        counties.append(county)
        counts.append([])
        index = len(counties) - 1
        if important == 1:
            important_counties.append(county)
    else:
        for i in range(len(counties)):
            if county == counties[i]:
                index = i
                break
    counts[index].append(cases)

# based on https://stackoverflow.com/questions/4534480/get-legend-as-a-separate-picture-in-matplotlib
fig, ax = plt.subplots(figsize=(11, 11))
ax.set_title('Cumulative Cases By GA County ' + str(datetime.now()))
for i in range(len(counts)):
    x = []
    y = []
    for j in range(len(counts[i])):
        x.append(j)
        y.append(counts[i][j])
    if counties[i] in important_counties:
        ax.plot(x, y, label=counties[i])
    else:
        ax.plot(x, y, color='#000000', label='_nolegend_')
ax.legend()
fig.show()
