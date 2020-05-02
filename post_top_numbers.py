import sqlite3
from urllib import request
import json
import sys
import datetime

connection = sqlite3.connect('caseupdates.sqlite')
cursor = connection.cursor()
cursor.execute("""SELECT NEW.COUNTY, (NEW.CASES - OLD.CASES) AS INCREASE
FROM CASES as NEW
INNER JOIN (
    SELECT COUNTY, CASES
    FROM CASES
    WHERE SET_ID = (
        SELECT MAX(SET_ID)
        FROM CASES
    ) - 1
) AS OLD ON OLD.COUNTY = NEW.COUNTY
WHERE NEW.SET_ID = (
    SELECT MAX(SET_ID) FROM CASES)
AND NEW.COUNTY != 'Unknown'
ORDER BY INCREASE DESC""");

text = ''
current_cases = 0
count = 0
while True:
    (county, cases) = cursor.fetchone()
    if current_cases == 0:
        current_cases = cases
    if current_cases == cases:
        text += f'{county}: {cases}\n'
        count += 1
    elif count >= 10:
        break
    else:
        text += f'{county}: {cases}\n'
        current_cases = cases
        count += 1

text = "{0}".format(f'Top Case Increases ({str(datetime.datetime.now())}):\n{text}')
text += "\n\nTop Death Increases:\n"

cursor.execute("""SELECT NEW.COUNTY, (NEW.DEATHS - OLD.DEATHS) AS INCREASE
FROM CASES as NEW
INNER JOIN (
    SELECT COUNTY, DEATHS
    FROM CASES
    WHERE SET_ID = (
        SELECT MAX(SET_ID)
        FROM CASES
    ) - 1
) AS OLD ON OLD.COUNTY = NEW.COUNTY
WHERE NEW.SET_ID = (
    SELECT MAX(SET_ID) FROM CASES)
AND NEW.COUNTY != 'Unknown'
AND INCREASE > 0
ORDER BY INCREASE DESC""");

count = 0
current_deaths = 0
while True:
    row = cursor.fetchone()
    if row is None:
        break
    (county, deaths) = row
    if current_cases == 0:
        current_deaths = deaths
    if current_deaths == deaths:
        text += f'{county}: {deaths}\n'
        count += 1
    elif count >= 10:
        break
    else:
        text += f'{county}: {deaths}\n'
        current_deaths = deaths
        count += 1

# based on https://www.accadius.com/send-message-slack-python-program/
post = {"text": text}

try:
    json_data = json.dumps(post)
    req = request.Request(sys.argv[1],
                          data=json_data.encode('ascii'),
                          headers={'Content-Type': 'application/json'})
    resp = request.urlopen(req)
except Exception as em:
    print("EXCEPTION: " + str.em)