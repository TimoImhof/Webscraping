import time
import ap_news_scraping
import tagesschau_scraping

while True:
    ap_news_scraping.start_retrieval()
    tagesschau_scraping.start_retrieval()
    time.sleep(14400) # execute script every 4 hours
