from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import html
from lxml.etree import tostring
from checkers import *


def serp_scraper(browser):
    try:
        # It doesn't catch rrs of 'Can birds smell'
        ## Search values
        source  = browser.page_source
        srctree = html.fromstring(source)
        button  = srctree.xpath('//button')
        query   = html.fromstring(tostring(list(button[0].iterancestors())[0])).xpath('//input//@value')
        query   = '|'.join(query)
        #####################################
        ####### Right Hand Side result ######
        #####################################
        rhs = {}
        rhs['title'] = '|'.join(srctree.xpath('//div[@id="rhs"]//div[@role="heading"]//text()'))
        rhs['url']   = ''.join(srctree.xpath('//div[@id="rhs"]//span/a/@href'))
        desc = srctree.xpath('//div[@id="rhs"]//div//span/text()')
        wc   = [len(t.split()) for t in desc]
        if wc:
            rhs['desc'] = desc[wc.index(max(wc))]
        else:
            rhs['desc'] = ""
        ############################
        ######## top result ########
        ############################
        trs = {}
        trs['title'] = '|'.join(srctree.xpath('(//div[@class="bkWMgd"])[1]//a/h3/text()'))
        trs['url']   = '|'.join(srctree.xpath('(//div[@class="bkWMgd"])[1]//cite/text()'))
        desc         = srctree.xpath('(//div[@class="bkWMgd"])[1]//div[@role="heading"]/span//text()')
        if not desc:
            desc         = srctree.xpath('(//div[@class="bkWMgd"])[1]//div/span[@class="st"]//text()')
        trs['desc'] = ' '.join(desc)
        ##################################
        ######## mid results #############
        ##################################
        # titles  = srctree.xpath('//div[@class="bkWMgd"]//div[@class="g" and ..//div[not(@class="srg")]]//a/h3/text()')
        xpath_part  = '//div[@class="bkWMgd" and position()>1]//div[@class="g" and not(ancestor::div[@class="srg"])]'
        mrs_titles = [''.join(srctree.xpath('(%s)[%s]//a/h3/text()' % (xpath_part, str(i)))) for i in range(1,len(srctree.xpath(xpath_part))+1)]
        mrs_descs  = [''.join(srctree.xpath('(%s)[%s]//span[@class="st"]//text()' % (xpath_part, str(i)))) for i in range(1,len(srctree.xpath(xpath_part))+1)]
        urls       = [''.join(srctree.xpath('(%s)[%s]//cite/text()' % (xpath_part, str(i)))) for i in range(1,len(srctree.xpath(xpath_part))+1)]
        urls_cl    = [''.join(srctree.xpath('(%s)[%s]//div[@class="r"]/a/@href' % (xpath_part, str(i)))) for i in range(1,len(srctree.xpath(xpath_part))+1)]
        mrs_urls   = url_cleaner(urls,urls_cl)
        ind        = [i for i,v in enumerate(mrs_descs) if v]
        mrs_titles = [mrs_titles[t] for t in ind]
        mrs_urls   = [mrs_urls[t] for t in ind]
        mrs_descs  = [mrs_descs[t] for t in ind]
        if(len(mrs_titles) != len(mrs_descs)): print('LOG: [CODE_ERROR(serp_scraper:mrs)] mrs_titles and mrs_descs don\'t match')
        #
        #
        ##################################
        ######## rest results ############
        ##################################
        titles  = srctree.xpath('//div[@class="bkWMgd"]//div[@class="srg"]//div[@class="g"]//a/h3/text()')
        urls    = srctree.xpath('//div[@class="bkWMgd"]//div[@class="srg"]//div[@class="g"]//cite/text()')
        urls_cl = srctree.xpath('//div[@class="bkWMgd"]//div[@class="srg"]//div[@class="g"]//div[@class="r"]/a/@href')
        urls    = url_cleaner(urls,urls_cl)
        # descs   = srctree.xpath('//div[@class="bkWMgd"]//div[@class="g"]//span[@class="st"]//text()')
        descs   = [' '.join(srctree.xpath('((//div[@class="bkWMgd"]//div[@class="srg"])//span[@class="st"])['+str(i)+']//text()')) \
        for i in range(1,len(srctree.xpath('((//div[@class="bkWMgd"]//div[@class="srg"])//span[@class="st"])'))+1)]
        ############################################
        ######## Appending mid and rest ############
        ############################################
        titles = mrs_titles + titles
        urls   = mrs_urls   + urls
        descs  = mrs_descs  + descs
        ############################################
        ############ Yielding results ##############
        ############################################
        rrs     = {i:{'title':v,'url':urls[i],'desc':descs[i]} for i,v in enumerate(titles)}
        serp    = {'top': trs, 'right':rhs, 'rest':rrs, 'query': query}
        return(serp)
    except:
        print('LOG: [SYSTEMIC(serp_scraper)] Attempt failed')
        return(serp_scraper(browser))



# for handle in browser.window_handles[0]:
#     browser.switch_to.window(handle)
#     print(browser.url)
