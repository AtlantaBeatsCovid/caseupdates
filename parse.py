import sqlite3
import datetime
import urllib3
import zipfile
import csv

http = urllib3.PoolManager()
response = http.request('GET', 'https://ga-covid19.ondemand.sas.com/docs/ga_covid_data.zip', preload_content=False)
zip_path = '/tmp/ga_covid_data.zip'
chunk_size = 4
with open(zip_path, 'wb') as out:
    while True:
        data = response.read(chunk_size)
        if not data:
            break
        out.write(data)

directory_path = '/tmp/ga_covid_data/'
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(directory_path)

csv_file_name = 'countycases.csv'
csv_path = directory_path + csv_file_name
with open(zip_path) as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    connection = sqlite3.connect('caseupdates.sqlite')
    cursor = connection.cursor()
    cursor.execute('select max(set_id) from CASES')
    set_id = cursor.fetchone()[0] + 1
    for row in reader:
        if row[0] != 'county_resident': # skip first line
            county = row[0]
            cases = row[1]
            deaths = row[2]
            cursor.execute(
                'INSERT INTO CASES (DATETIME, COUNTY, CASES, DEATHS, SET_ID) VALUES (?, ?, ?, ?, ?)',
                (str(datetime.datetime.now()), county, int(cases), int(deaths), int(set_id))
            )
    connection.commit()
    connection.close()
