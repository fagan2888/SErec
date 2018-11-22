

# Template
# Open browser and type google.com

# waiter
## call is_open_browser
## if True wait until page changes
## if False save observer to JSON

# call waiter

# check if it is a google SERP
## If so call serp_scraper
## set querynum += 1
### append {querynum: serp_scraper output}
### call is_open_browser
### call waiter
## If not wait until page changes

# after google SERP (waiter is active)
# If waiter -> page_change
## check if a click
### If a click, scrape the html and url
### choice += 1
### match the url in SERP -> rank \in {top, rhs, 'rrs'+rrsRank}
### clickres = {'rank': rank, 'url':url, 'page':html}
### append observer[querynum][choice] = clickres
### call waiter
###
## if not a click
## if a SERP
## If so call serp_scraper
## set querynum += 1
### append {querynum: serp_scraper output}
### call waiter
##
