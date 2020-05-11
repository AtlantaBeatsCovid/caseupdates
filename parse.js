const puppeteer = require('puppeteer');

(async () => {
  try {
    const browser = await puppeteer.launch({
      // headless: false
    });
    const page = await browser.newPage();
    await page.goto('https://ga-covid19.ondemand.sas.com/');
    await page.waitForSelector(
        '#react-tabs-5 > div > div > table > tbody > ' +
        'tr:nth-child(1) > td.MuiTableCell-root.MuiTableCell-body.MuiTableCell-' +
        'alignLeft.MuiTableCell-sizeSmall', {
          visible: true,
        });
    const html = await page.content();
    const myregexp = /<td class="MuiTableCell-root MuiTableCell-body MuiTableCell-alignLeft MuiTableCell-sizeSmall" style="border: none;">([a-zA-Z ]+)<\/td><td class="MuiTableCell-root MuiTableCell-body MuiTableCell-alignRight MuiTableCell-sizeSmall" style="border: none;">(\d+)<\/td><td class="MuiTableCell-root MuiTableCell-body MuiTableCell-alignRight MuiTableCell-sizeSmall" style="border: none;">[.\d-]+<\/td><td class="MuiTableCell-root MuiTableCell-body MuiTableCell-alignRight MuiTableCell-sizeSmall" style="border: none;">(\d+)/g;
    let match = myregexp.exec(html);
    const db = require('better-sqlite3')('caseupdates.sqlite');
    const row = await db.prepare('select max(set_id) as setId from CASES').get();
    const setId = row.setId + 1;
    const insert = db.prepare('INSERT INTO CASES (DATETIME, COUNTY, CASES, DEATHS, SET_ID) VALUES (?, ?, ?, ?, ?)');
    while (match != null) {
      const d = new Date();
      const datestring = (d.getFullYear()) + "-" + ("0"+(d.getMonth()+1)).slice(-2) + "-"
          + ("0" + d.getDate()).slice(-2) + " " + ("0" + d.getHours()).slice(-2) + ":" + ("0" + d.getMinutes()).slice(-2)
          + ":" + ("0" + d.getSeconds()).slice(-2) + ".000000";
      insert.run(datestring, `${match[1]}`, `${match[2]}`, `${match[3]}`, setId);
      match = myregexp.exec(html);
    }
    await db.close();
    await browser.close();
  } catch (error) {
    console.log(error);
  }
})();
