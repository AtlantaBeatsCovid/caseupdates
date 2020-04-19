import urllib.request
import logging
import re
import sqlite3
import datetime

with urllib.request.urlopen('https://dph.georgia.gov/covid-19-daily-status-report') as main_response:
    outer_result = re.search(
        r"\s*var pymParent = new pym\.Parent\('covid19dashdph', '(.+)', \{'title':'COVID-19 Daily Status Report'\}\);",
        main_response.read().decode(), re.IGNORECASE)
    if outer_result:
        inner_url = outer_result.group(1)
        with urllib.request.urlopen(inner_url) as inner_response:
            inner_result = re.search(
                r'COVID-19 Confirmed Cases By County:</td><td class="tcellh">No\. Cases</td><td class="tcellh">No\. Deaths</td></tr>(.*?)</table>',
                inner_response.read().decode(), re.IGNORECASE | re.DOTALL)
            if inner_result:
                html_data = inner_result.group(1)
                connection = sqlite3.connect('caseupdates.sqlite')
                cursor = connection.cursor()
                for match in re.finditer(
                    r'<tr><td class="tcell">(\w+)</td><td class="tcell">(\d+)\s*</td><td class="tcell">(\d+)\s*</td></tr>',
                    html_data, re.IGNORECASE):

                    county = match.group(1)
                    cases = match.group(2)
                    deaths = match.group(3)

                    cursor.execute(
                        'INSERT INTO CASES (DATETIME, COUNTY, CASES, DEATHS) VALUES (?, ?, ?, ?)',
                        (str(datetime.datetime.now()), county, int(cases), int(deaths))
                    )
                connection.commit()
                connection.close()
            else:
                logging.error("Can't find data.")
    else:
        logging.error("Can't find data url.")
