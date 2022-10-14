import urllib.request, sys, time
from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import locale

locale.setlocale(locale.LC_TIME, "de_DE")

url_1 = 'https://www.tagesschau.de/archiv/'
url_2 = '?datum=2022-03-04'


def modifyHTML(param):
    ''' TODO: implement'''
    pass

def load_next_day(soup):
    date_string = soup.find('h2', attrs={'class': 'archive__headline'}).text
    date = time.strptime(date_string, '%d. %B %Y')
    print(date)

def extract_all():
    ''' TODO: implement'''
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

page = load_page(url_1, url_2)
soup = BeautifulSoup(page.text, "html.parser")
load_next_day(soup)

numb_results = soup.find('span', attrs={'class': 'ergebnisse__anzahl'}).text.strip()

''' rough code structure

for year in archive:
    for month in year:
        if numb_results is 0:
            load_next_day()
        else:
            extract_all()
'''
