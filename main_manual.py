from selenium import webdriver
from lxml import html
from serp_scraper import *
from checkers import *
from time import sleep

# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.remote.command import Command
# from selenium.webdriver.support import expected_conditions as EC
import http.client as httplib
import socket

# Code

# Open browser and type google.com
browser = webdriver.Firefox()
browser.get('https://www.google.com')
browser.current_url

choice    = 0
querynum  = 0
global observer  = {}
cur_query = ''

# call waiter
waiter(browser) # passed initial test

# check if it is a google SERP
# after google SERP (waiter is active)
# If waiter -> page_change
## check if a click

sleep(2)

is_google = check_if_google(browser) # fails at first attempt


if is_google == 'serp':
    print('LOG: It is a SERP')
    serp = serp_scraper(browser)
    serp_logger(serp)
    print('\n')
    if serp['query'] == cur_query:
        print('LOG: Returned back to the same query, waiting')
        waiter(browser)
    else:
        querynum += 1
        cur_query = serp['query']
        observer[querynum] = serp
        print('LOG: A new query, scraped, waiting')
        waiter(browser)
elif is_google == 'google':
    print('LOG: Google page, waiting')
    waiter(browser)
    print(len(observer))
else:
    # is equivalent to is_google == 'not':
    ### If a click, scrape the html and url and increase choice
    ### match the url in SERP -> rank \in {top, rhs, 'rrs'+rrsRank}
    ### clickres = {'rank': rank, 'url':url, 'page':html}
    ### append observer[querynum][choice] = clickres
    choice += 1
    rank = match_url(browser.current_url,observer[querynum])
    clickres = {'rank': rank, 'url':browser.current_url, 'page':browser.page_source}
    observer[querynum][choice] = clickres
    choice_logger(choice)
    print('LOG: clickres rank:', clickres['rank'])
    print('LOG: clickres url:', clickres['url'])
    ### call waiter
    waiter(browser)
