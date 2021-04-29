"""
Created by Manuel Silverio

Example of Web scraper for Booking.com Hotel info for 2 adults and 1 night

Location is set to London. the script will fetch by default the next day from the request current time

The duration will be 1 night by default with 2 adults.

Booking.com uses location IDs ... changing the location is a bit tricky but can be done.

"""

from selectorlib import Extractor
import requests
import pandas as pd
from datetime import timedelta, datetime


date_checkin = datetime.now() + timedelta(days=1)
date_checkout = datetime.now() + timedelta(days=2)
day_check_in = date_checkin.day
day_check_out =date_checkout.day
month_check_in = date_checkin.month
month_check_out = date_checkout.month
year_checkin = date_checkin.year
year_checkout = date_checkout.year
adults = 2
location = ''


url = 'https://www.booking.com/searchresults.en-gb.html?' \
      '&ssne=London&ssne_untouched=London&dest_id=-2601889&dest_type=city' \
      '&checkin_year={}&checkin_month={}&checkin_monthday={}&checkout_year={}&checkout_month={}&checkout_monthday={}' \
      '&group_adults={}&group_children=0&no_rooms=1&b_h4u_keep_filters=&from_sf=1'\
    .format(year_checkin,month_check_in, day_check_in, year_checkout, month_check_out, day_check_out, adults)

# Create an Extractor by reading from the YAML file
e = Extractor.from_yaml_file('booking.yml')


def scrape(url):    
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        # You may want to change the user agent if you get blocked
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',

        'Referer': 'https://www.booking.com/index.en-gb.html',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    print("Downloading %s"%url)
    r = requests.get(url, headers=headers)
    # Pass the HTML of the page and create 
    return e.extract(r.text,base_url=url)


data = scrape(url)
if data:
    df = pd.DataFrame(data['hotels'])
    df.to_csv('example_output.csv')