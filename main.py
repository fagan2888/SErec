from selenium import webdriver
from lxml import html
from serp_scraper import *
from checkers import *
from time import sleep
import http.client as httplib
import socket

# Code

## Prior judgement
q,a = prior_questionaire()


# Open browser and type google.com
browser = webdriver.Firefox()
browser.get('https://www.google.com')
browser.current_url
browserIsOpen = True

choice    = 0
querynum  = 0
observer  = {'metadata':{'main_query':q, 'prior_answer':a}}
cur_query = ''

# call waiter
waiter(browser,observer) # passed initial test

# check if it is a google SERP
# after google SERP (waiter is active)
# If waiter -> page_change
## check if a click



while browserIsOpen:
    is_google = check_if_google(browser) # fails at first attempt
    if is_google == 'serp':
        print('LOG: It is a SERP')
        serp = serp_scraper(browser)
        serp_logger(serp)
        print('\n')
        if serp['query'] == cur_query:
            print('LOG: Returned back to the same query, waiting')
            waiter(browser,observer)
        else:
            querynum += 1
            choice    = 0
            cur_query = serp['query']
            observer[querynum] = serp
            print('LOG: A new query, scraped, waiting')
            waiter(browser,observer)
    elif is_google == 'google':
        print('LOG: Google page, waiting')
        print(len(observer))
        waiter(browser,observer)
    elif is_google == 'not':
        # is equivalent to is_google == 'not':
        ### If a click, scrape the html and url and increase choice
        ### match the url in SERP -> rank \in {top, rhs, 'rrs'+rrsRank}
        ### clickres = {'rank': rank, 'url':url, 'page':html}
        ### append observer[querynum][choice] = clickres
        choice += 1
        rank = match_url(browser.current_url,observer[querynum])
        clickres = {'rank': rank, 'url':browser.current_url, 'page':''}
        observer[querynum][choice] = clickres
        choice_logger(choice)
        print('LOG: clickres rank:', clickres['rank'])
        print('LOG: clickres url:', clickres['url'])
        ### call waiter
        waiter(browser,observer)
    else:
        print('LOG[main] Status:', is_google)
        waiter(browser,observer)
    browserIsOpen = is_open(browser)

print('LOG: Session ended')
