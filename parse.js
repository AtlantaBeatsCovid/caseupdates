const puppeteer = require('puppeteer');

(async () => {
  try {
    const browser = await puppeteer.launch({
      headless: false
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
    const myregexp = /<td class="MuiTableCell-root MuiTableCell-body MuiTableCell-alignLeft MuiTableCell-sizeSmall" style="border: none;">(\w+)<\/td><td class="MuiTableCell-root MuiTableCell-body MuiTableCell-alignRight MuiTableCell-sizeSmall" style="border: none;">(\d+)<\/td><td class="MuiTableCell-root MuiTableCell-body MuiTableCell-alignRight MuiTableCell-sizeSmall" style="border: none;">[.\d-]+<\/td><td class="MuiTableCell-root MuiTableCell-body MuiTableCell-alignRight MuiTableCell-sizeSmall" style="border: none;">(\d+)/g;
    let match = myregexp.exec(html);
    while (match != null) {
      console.log(`${match[1]}:${match[2]}:${match[3]}`);
      match = myregexp.exec(html);
    }

    await browser.close();
  } catch (error) {
    console.log(error);
  }
})();
