import urllib.request, sys, time
from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt

url_1 = 'https://www.tagesschau.de/archiv/'
url_2 = '?datum=2003-01-01'
url_3 = '&ressort=wirtschaft'
url = url_1 + url_2 + url_3


def load_next_month():
    date_string = soup.find('h2', attrs={'class': 'archive__headline'}).text
    date = time.strptime(string=date_string, format='%B %Y')
    print(date_string)
    print(date)


def extract_all():
    return ''


try:
    # this might throw an exception if something goes wrong.
    page = requests.get(url)
    # this describes what to do if an exception is thrown
    if page.status_code.__eq__(200):
        print("Page loaded successfully!")
    print(page.headers.get("content-type", 'unknown'))
except Exception as e:

    # get the exception information
    error_type, error_obj, error_info = sys.exc_info()

    # print the link that cause the problem
    print('ERROR FOR LINK:', url)

    # print error info and line that threw the exception
    print(error_type, 'Line:', error_info.tb_lineno)

soup = BeautifulSoup(page.text, "html.parser")

numb_results = soup.find('span', attrs={'class': 'ergebnisse__anzahl'}).text.strip()
load_next_month()

''' rough code structure

for year in archive:
    for month in year:
        if numb_results is 0:
            load_next_month()
        else:
            extract_all()
'''
