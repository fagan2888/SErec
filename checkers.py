from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.command import Command
from selenium.webdriver.support import expected_conditions as EC
from lxml import html
import http.client as httplib
import socket, re, json
from time import sleep
from http.client import RemoteDisconnected
from selenium.common.exceptions import *
from main import *
from datetime import datetime

def check_browser_open(browser):
    try:
        browser.current_url
        browser.execute(Command.STATUS)
        return(True)
    except (SessionNotCreatedException, WebDriverException, NoSuchWindowException,\
    httplib.CannotSendRequest, ConnectionRefusedError,httplib.RemoteDisconnected,\
    socket.error):
        return(False)

main_query   = ''
prior_answer = ''
post_answer  = ''

def output_namer():
    global main_query
    dt = datetime.now().isoformat()
    outputName = main_query + dt
    outputName = str(outputName.__hash__())
    outputName = '_'.join(main_query.split()[:3]) + outputName + '.json'
    print(outputName)
    return(outputName)


choices = '1. Strongly disagree\n2. Disagree\n3. Indifferent/Not sure\n4. Agree\n5. Strongly Agree\n> '

def prior_questionaire():
    global main_query
    global prior_answer
    main_query   = input('Enter the given query:\n> ')
    prior_answer = input('How much do you agree (Choose between 1-5):\n\n{}\n\n{}'.format(main_query,choices))
    return(main_query,prior_answer)

def post_questionaire():
    global main_query
    post_answer = input('How much do you agree (Choose between 1-5):\n\n{}\n\n{}'.format(main_query,choices))
    return(post_answer)

def session_saver(observer):
    answer = post_questionaire()
    observer['metadata']['post_answer'] = answer
    outputName = output_namer()
    with open(outputName, 'w') as fh:
        json.dump(observer,fh)

def is_open(browser):
    attempt1 = check_browser_open(browser)
    attempt2 = check_browser_open(browser)
    attempt3 = check_browser_open(browser)
    return(attempt1 or attempt2 or attempt3)


def waiter(browser,observer):
    test_dict = observer
    browserIsOpen = is_open(browser)
    print(browserIsOpen)
    try:
        if browserIsOpen==True:
            n=30
            WebDriverWait(browser, n*60).until(EC.url_changes(browser.current_url))
        else:
            print('LOG: Browser is closed, saving the file')
            # outputName = 'test.json'
            # with open(outputName, 'a') as fh:
                # json.dump(test_dict,fh)
            session_saver(observer)
    except:
        sleep(2)
        print('LOG[*(waiter)] An error occured, recalling waiter')
        return(waiter(browser,observer))

def check_if_google(browser):
    sleep(1)
    try:
        srctree = html.fromstring(browser.page_source)
        url     = browser.current_url
        check       = url.startswith('https://www.google') or (srctree.xpath('//div[@id="searchform"]') and srctree.xpath('//img[@alt="Google"]'))
        checkSERP   = srctree.xpath('//div[@id="search"]')
        if checkSERP:
            isgoogle = 'serp'
        elif check:
            isgoogle = 'google'
        else:
            isgoogle = 'not'
        return(isgoogle)
    except:
        print('LOG: [SYSTEMIC] Attempt failed')
        if is_open(browser):
            return(check_if_google(browser))
        else:
            return('nobrowser')

def match_url(url,serp):
    istrs   = serp['top']['url'] == url
    isrhs   = serp['right']['url'] == url
    rrs     = serp['rest']
    rrsUrls = [rrs[i]['url'] for i in range(len(rrs))]
    try:
        rrsRank = rrsUrls.index(url)
    except(ValueError):
        rrsRank = None
    rank = []
    if istrs: rank.append('top')
    if isrhs: rank.append('right')
    if rrsRank is not None: rank.append('rrs' + str(rrsRank))
    if rank:
        out = ';'.join(rank)
    else:
        out = None
        print('LOG: Rank not found')
    return(out)

def serp_logger(serp):
    ctop   = [len(v) for v in serp['top'].values()]
    cright = [len(v) for v in serp['right'].values()]
    crest  = [len(v) for v in serp['rest'].values()]
    print('LOG: Query scraped', len(serp['query']) > 0)
    print('LOG: Top scraped', sum(ctop) > 0)
    print('LOG: Right scraped', sum(cright) > 0)
    print('LOG: Rest scraped', sum(crest) > 0)

def choice_logger(choice):
    if choice == 0:
        print('No choice yet')
    elif choice == 1:
        print('LOG: The first choice')
    else:
        print('LOG: Next choice, #', choice)

def url_cleaner(urls,urls_cl):
    ## There are two types of urls can be retrieved by SERP, cite that SERP displays
    ## and a href's. Retrieving both, choosing one.
    ## Cutting a href's fro &usg, replacing if citations end with ... or not begin with http.
    urls_cl = [''.join(re.findall('http.*$',url)) for url in urls_cl]
    urls_cl = [re.sub('&usg.*','',url).replace('%3A',':').replace('%2F','/') for url in urls_cl]
    #
    if(len(urls) == len(urls_cl)):
        ind = [urls.index(url) for url in urls if not url.startswith('http') or \
        '...' in url or ' ' in url]
        for i in ind:
            urls[i] = urls_cl[i]
    else:
        print('LOG: [CODE_ERROR(url_cleaner)] urls and urls_scraped are not matching')
    return(urls)
