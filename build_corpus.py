import time
import urllib.request, sys
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import locale


def modify_HTML(param):
    """ TODO: implement"""
    pass


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
            return create_new_link(new_date.date().year, new_date.date().month, new_date.date().day), new_date
        else:
            new_date = datetime.strptime(date_string, '%B %Y') + relativedelta(months=1)
            return create_new_link(new_date.date().year, new_date.date().month), new_date

    except Exception as e:

        error_type, error_obj, error_info = sys.exc_info()
        print(error_obj)
        print('Date format has changed from "Month Year" to "Day. Month Year"!')
        new_date_format = True
        new_date = datetime.strptime(date_string, '%d. %B %Y') + timedelta(days=1)
        return create_new_link(new_date.date().year, new_date.date().month, new_date.date().day), new_date


def extract_all():
    """ TODO: implement"""
    pass


def load_page(url_1, url_2):
    ''' TODO: '''
    url = url_1 + url_2
    try:
        # this might throw an exception if something goes wrong.
        page = requests.get(url)
        # this describes what to do if an exception is thrown
        if page.status_code.__eq__(200):
            print("Page loaded successfully!")
        print(page.headers.get("content-type", 'unknown'))
        return page
    except Exception as e:

        # get the exception information
        error_type, error_obj, error_info = sys.exc_info()

        # print the link that cause the problem
        print('ERROR FOR LINK:', url)

        # print error info and line that threw the exception
        print(error_type, 'Line:', error_info.tb_lineno)

'''--- Retrieval Session ---'''

locale.setlocale(locale.LC_TIME, "de_DE")

url_1 = 'https://www.tagesschau.de/archiv/'
url_2 = '?datum=2021-12-01'
new_date_format = False

'''code structure'''
print(date.today())


while date.date() is not date.today():
    
    page = load_page(url_1, url_2)
    soup = BeautifulSoup(page.text, "html.parser")
    numb_results = soup.find('span', attrs={'class': 'ergebnisse__anzahl'}).text.strip()
    
    if numb_results == 0:
        continue
    else:
        extract_all()

    url_2, date = load_next_day(soup, new_date_format)