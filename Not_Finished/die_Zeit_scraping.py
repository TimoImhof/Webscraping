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

locale.setlocale(locale.LC_TIME, "de_DE")
start_url = 'https://www.zeit.de/2017/index'
actual_date = datetime.strptime('20. Oktober 2022', '%d. %B %Y')
search_date = datetime.strptime('1. Oktober 2019', '%d. %B %Y')


def extract_all_content(start_url):
    """ TODO: """
    url = start_url
    while search_date.date() != actual_date.date():
        # year loop
        soup = get_soup(url)
        edition_links = get_links(soup, 'a', 'teaser-volume-overview__link')
        for edition in edition_links:
            # edition loop for each year
            edition_soup = get_soup(edition)
            article_links = get_links(edition_soup, 'div', 'teaser-small  has-bookmark-icon')
        url = get_next_index_url(soup)


def get_right_areas(soup):
    """ TODO: """
    wanted_areas = []
    areas = soup.find_all('div', attrs={'class': 'cp-region cp-region--solo'})
    for area in areas:
        if area.find('h2', attrs={'class': 'cp-area__headline'}) is not None:
            topic = area.find('h2', attrs={'class': 'cp-area__headline'}).text
            if topic == 'Politik' or 'Wirtschaft' or 'Wissen' or 'Recht und Unrecht':
                wanted_areas.append(area)
    return wanted_areas


def get_links(soup, tag_type, class_name):
    """ Takes Beautifulsoup object, and two objects of type string and returns list contaning all strings (url) of
    specified tag and class. """
    links = []
    overview = soup.find('div', attrs={'class': 'volume-overview'})
    for link in overview.find_all(tag_type, attrs={'class': class_name}):
        links.append(link['href'])
    return links


def get_next_index_url(soup):
    """ Takes Beautifulsoup object, searches HTML for current index(year) and new url with next year"""
    current_year = soup.find('li', attrs={'class': 'pager__page pager__page--current'}).text.strip()
    current_year = int(current_year) + 1
    return 'https://www.zeit.de/' + str(current_year) + '/index'


def get_soup(url):
    """ Takes an url as string and returns a Beautifulsoup object from this url."""
    try:
        time.sleep(2)
        page = requests.get(url)
        return BeautifulSoup(page.text, 'html.parser')
    except Exception as e:
        print('Could not load page!')
        return -1

print(len(get_right_areas(get_soup('https://www.zeit.de/2017/01/index'))))
