import time
import urllib.request, sys
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import locale
import csv


def get_links(soup):
    """ Takes Beautifulsoup object, and returns list contaning all url of that contain a substring 'article. """
    links = []
    overview = soup.find('div', attrs={'class': 'Body'})
    for link in overview.find_all('a'):
        links.append('https://apnews.com' + link['href'])
    links = list(set(links))
    article_links = []
    for link in links:
        if 'article' in link:
            article_links.append(link)
    return article_links


def get_soup(url):
    """ Takes an url as string and returns a Beautifulsoup object from this url."""
    try:
        time.sleep(2)
        page = requests.get(url)
        return BeautifulSoup(page.text, 'html.parser')
    except Exception as e:
        print('Could not load page!')
        return -1


def get_search_date():
    """ TODO: implement"""
    pass


def get_article_content(url):
    """ TODO: implement"""
    pass


soup = get_soup('https://apnews.com/hub/business?utm_source=apnewsnav&utm_medium=navigation')
links = get_links(soup)
print(len(links))
