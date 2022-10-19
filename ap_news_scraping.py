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


def get_links(soup, tag_type, class_name):
    """ Takes Beautifulsoup object, and two objects of type string and returns list contaning all strings (url) of
    specified tag and class. """
    links = []
    overview = soup.find('div', attrs={'class': 'volume-overview'})
    for link in overview.find_all(tag_type, attrs={'class': class_name}):
        links.append(link['href'])
    return links


def get_soup(url):
    """ Takes an url as string and returns a Beautifulsoup object from this url."""
    try:
        time.sleep(2)
        page = requests.get(url)
        return BeautifulSoup(page.text, 'html.parser')
    except Exception as e:
        print('Could not load page!')
        return -1
