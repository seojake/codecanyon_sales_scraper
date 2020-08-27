import time, schedule, requests
from datetime import datetime
from bs4 import BeautifulSoup
from sql import *

## Function to run
def check_sales():
    ## Get the URLs from the urls.txt file
    urls = open('/Applications/MAMP/htdocs/codecanyon-sale-checker/urls.txt', 'r');

    ## Set some headers so we don't look too spammy..
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

    ## Only run if there is URLs to loop
    if(urls):
        for url in urls.readlines():
            request = requests.get(url, headers) ## Request the page
            html = BeautifulSoup(request.content, 'html.parser') ## Store the HTML from the request in a variable
            todays_sales = html.select_one('.sidebar-stats__number').text.strip().encode('ascii').replace(',', '') ## Store todays sales in a variable
            item = html.select_one('h1.t-heading').text.strip().encode('ascii') ## Store the item name in a variable

            ## Store the scraped data in the database
            db_exe.execute("INSERT INTO sales (url, item, sales) VALUES (%s, %s)", (url, item, todays_sales,))
            db_conn.commit()

## Run the scraper function every night at 9pm
## You can change '21:00' to any time you wish, just ensure it used the 24hr format
schedule.every().day.at('21:00').do(check_sales)

## Run all the pending tasks in the schedule
## Wait 60 seconds after before performing the other tasks
while True:
    schedule.run_pending()
    time.sleep(60)
