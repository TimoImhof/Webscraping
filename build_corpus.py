import time
import urllib.request, sys
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import locale

'''--- Methods ---'''


def create_new_link(year, month, day=None):
    """ Create new URL by inserting parameters in URL format"""
    if day is None:
        print('Next Date is:' + '?datum=' + str(year) + '-' + str(month).zfill(2) + '-01')
        return '?datum=' + str(year) + '-' + str(month).zfill(2) + '-01'
    else:
        print('Next Date is:' + '?datum=' + str(year) + '-' + str(month).zfill(2) + '-' + str(day).zfill(2))
        return '?datum=' + str(year) + '-' + str(month).zfill(2) + '-' + str(day).zfill(2)


def load_next_day(soup, is_new_format):
    date_string = soup.find('h2', attrs={'class': 'archive__headline'}).text

    try:
        if is_new_format:
            new_date = datetime.strptime(date_string, '%d. %B %Y') + timedelta(days=1)
            return create_new_link(new_date.date().year, new_date.date().month, new_date.date().day), new_date, True
        else:
            new_date = datetime.strptime(date_string, '%B %Y') + relativedelta(months=1)
            return create_new_link(new_date.date().year, new_date.date().month), new_date, False

    except Exception as e:

        error_type, error_obj, error_info = sys.exc_info()
        print(error_obj)
        print('Date format has changed from "Month Year" to "Day. Month Year"!')
        new_date = datetime.strptime(date_string, '%d. %B %Y') + timedelta(days=1)
        return create_new_link(new_date.date().year, new_date.date().month, new_date.date().day), new_date, True


def extract_all(soup):
    """ TODO: implement"""
    block = soup.find_all('a', attrs={'class': 'teaser-xs__link'})
    links = []
    for article_links in block:
        links.append(article_links['href'])
    return links

def load_page(url_1, url_2):
    """ TODO: """
    url = url_1 + url_2
    try:
        time.sleep(2)
        page = requests.get(url)
        return page
    except Exception as e:
        error_type, error_obj, error_info = sys.exc_info()
        # print the link that cause the problem
        print('ERROR FOR LINK:', url)
        # print error info and line that threw the exception
        print(error_type, 'Line:', error_info.tb_lineno)


'''--- Retrieval Session ---'''

locale.setlocale(locale.LC_TIME, "de_DE")

url_1 = 'https://www.tagesschau.de/archiv/'
url_2 = '?datum=2022-10-14'
new_date_format = False
actual_date = datetime.strptime('15. Oktober 2022', '%d. %B %Y')
search_date = datetime.strptime('14. Oktober 2022', '%d. %B %Y')

'''code structure'''

while search_date.date() != actual_date.date():

    page = load_page(url_1, url_2)
    soup = BeautifulSoup(page.text, "html.parser")
    numb_results = soup.find('span', attrs={'class': 'ergebnisse__anzahl'}).text.strip()

    if numb_results == 0:
        continue
    else:
        print(extract_all(soup))

    url_2, search_date, new_date_format = load_next_day(soup, new_date_format)
