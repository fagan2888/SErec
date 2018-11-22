from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import html




browser = webdriver.Firefox()
browser.get('https://www.google.com')

browser.current_url



WebDriverWait(browser, 600).until(EC.url_changes(browser.current_url))

def check_if_google(browser):
    srctree = html.fromstring(browser.page_source)
    url     = browser.current_url
    check   = url.startswith('https://www.google') or (srctree.xpath('//div[@id="searchform"]') and srctree.xpath('//img[@alt="Google"]'))
    return(check)


## Search values
source  = browser.page_source
srctree = html.fromstring(source)
query   = '|'.join(srctree.xpath('//div[@id="gs_lc0"]/input/@value'))

## Right Hand Side result
rhs = {}
rhs['title'] = '|'.join(srctree.xpath('//div[@id="rhs"]//div[@role="heading"]//text()'))
rhs['url']   = ''.join(srctree.xpath('//div[@id="rhs"]//span/a/@href'))
desc = srctree.xpath('//div[@id="rhs"]//div//span/text()')
wc   = [len(t.split()) for t in desc]
if wc:
    rhs['desc'] = desc[wc.index(max(wc))]
else:
    rhs['desc'] = ""

## top result
trs = {}
trs['title'] = '|'.join(srctree.xpath('(//div[@class="bkWMgd"])[1]//a/h3/text()'))
trs['url']   = '|'.join(srctree.xpath('(//div[@class="bkWMgd"])[1]//cite/text()'))
desc         = srctree.xpath('(//div[@class="bkWMgd"])[1]//div[@role="heading"]/span//text()')
trs['desc'] = ' '.join(desc)

## rest results
titles = srctree.xpath('(//div[@class="bkWMgd"])[3]//a/h3/text()')
urls   = srctree.xpath('(//div[@class="bkWMgd"])[3]//cite/text()')
descs  = [' '.join(srctree.xpath('((//div[@class="bkWMgd"])[3]//span[@class="st"])['+str(i)+']//text()')) for i in range(1,len(urls)+1)]
rrs    = {i+1:[v,urls[i],descs[i]] for i,v in enumerate(titles)}


# for handle in browser.window_handles[0]:
#     browser.switch_to.window(handle)
#     print(browser.url)
