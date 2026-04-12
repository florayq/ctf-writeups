const puppeteer = require('puppeteer');
require('dotenv').config();

const FLAG = process.env.FLAG;

async function checkUrl(targetUrl, vulnIndex) {
    const browser = await puppeteer.launch({
        headless: "new",
        executablePath: process.env.PUPPETEER_EXECUTABLE_PATH || 'chromium',
        args: [
            '--no-sandbox', 
            '--disable-setuid-sandbox', 
            '--disable-gpu',
            '--disable-dev-shm-usage'
        ]
    });

    try {
        const page = await browser.newPage();

        page.on('console', msg => console.log(msg.text()));

        const parsedUrl = new URL(targetUrl);
        
        await page.setCookie({
            name: 'flag',
            value: FLAG,
            domain: parsedUrl.hostname,
            path: '/',
            httpOnly: false,
            secure: false,
            sameSite: 'Lax'
        });


        await page.goto(targetUrl, { 
            waitUntil: 'domcontentloaded', 
            timeout: 15000 
        });

        await new Promise(r => setTimeout(r, 5000));

    } catch (e) {
    } finally {
        await browser.close();
    }
}

if (require.main === module) {
    const args = process.argv.slice(2);
    if (args.length >= 2) {
        checkUrl(args[0], args[1]);
    }
}