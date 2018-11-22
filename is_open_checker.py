from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.command import Command
from selenium.webdriver.support import expected_conditions as EC
from lxml import html
import http.client as httplib
import socket, re
from time import sleep
from selenium.common.exceptions import *
from selenium import webdriver


def check_browser_open(browser):
    # try:
        try:
            browser.current_url
            return(True)
        except (SessionNotCreatedException, WebDriverException, socket.error,\
        httplib.CannotSendRequest, ConnectionRefusedError,httplib.RemoteDisconnected):
            return(False)
    # except:
        # return(check_browser_open(browser))

browser = webdriver.Firefox()
browser.get('https://www.google.com')



while True:
    check_browser_open(browser)
    sleep(.5)
