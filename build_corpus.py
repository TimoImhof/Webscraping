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

'''--- Methods ---'''


def create_new_link(year, month, day=None):
    """ Create new URL by inserting parameters in URL format"""
    if day is None:
        return '?datum=' + str(year) + '-' + str(month).zfill(2) + '-01'
    else:
        return '?datum=' + str(year) + '-' + str(month).zfill(2) + '-' + str(day).zfill(2)


def load_next_day(soup_object, is_new_format):
    """  Takes Beautifulsoup object and boolean which indicates the date format.
     Extracts the current date of the loaded webpage and increments it:\n
     - old date format: increment per one month
     - new date format: increment per one day
     Returns new link part containing the actualized date."""
    date_string = soup_object.find('h2', attrs={'class': 'archive__headline'}).text

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


def extract_article_links(soup_object, link):
    """ Takes Beautifulsoup object and extracts all article links on a webpage and returns them in a list."""

    block = soup_object.find_all('a', attrs={'class': 'teaser-xs__link'})
    links = []
    for article_links in block:
        links.append(article_links['href'])

    return links


def load_page(url):
    """ Takes url as string and sends request to webpage."""
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


def retrieve_article_content(soup_object):
    """ Takes an Beautifulsoup object and returns all written text as one string"""
    article = soup_object.find('article', attrs={'class': 'container content-wrapper__group'})
    topline = article.find('span', attrs={'class': 'seitenkopf__topline'}).text.strip()
    headline = article.find('span', attrs={'class': 'seitenkopf__headline--text'}).text.strip()
    text = ''
    for para in article.find_all('p', attrs={'class': 'm-ten m-offset-one l-eight l-offset-two textabsatz columns '
                                                      'twelve'}):
        text = text + para.text.strip() + ' '
    print(topline + ' | ' + headline)
    return topline, headline, text


def save_content_to_csv(content, date):
    """ Takes list of lists as content and string as date and writes content to new csv file named after string."""
    header = ['topline', 'headline', 'content']
    directory = 'C:\\Users\\Timo\\PycharmProjects\\Webscraping\\Tagesschau_archive\\'
    with open(file=directory + 'tagesschau_' + date + '.csv', mode='x', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for article in content:
            writer.writerow([article[0], article[1], article[2]])


def has_results(soup_object):
    """ Takes Beautifulsoup object and extracts number of article links.
    Returns False if there are no links, otherwise True."""
    numb_results = soup_object.find('span', attrs={'class': 'ergebnisse__anzahl'}).text.strip()
    return int(numb_results) != 0


'''--- Retrieval Session ---'''

locale.setlocale(locale.LC_TIME, "de_DE")

url_1 = 'https://www.tagesschau.de/archiv/'
url_2 = '?datum=2005-01-01'
actual_date = datetime.strptime('18. Oktober 2021', '%d. %B %Y')
search_date = datetime.strptime('17. Oktober 2020', '%d. %B %Y')

new_date_format = False
article_links = []

'retrieve all article links: '

while search_date.date() != actual_date.date():
    print(search_date.date())
    page = load_page(url_1 + url_2)
    soup = BeautifulSoup(page.text, "html.parser")
    print("loaded archive page...")
    print(has_results(soup))

    if has_results(soup):
        articles = []
        article_links = extract_article_links(soup)
        print('got all article links...')
        day_string = search_date.date().strftime('%Y-%m-%d')

        print('start extracting content from links...')
        for link in article_links:
            link_page = load_page(link)
            link_soup = BeautifulSoup(link_page.text, 'html.parser')
            topline, headline, content = retrieve_article_content(link_soup)
            articles.append([topline, headline, content])
        print('finished extraction... \n proceed to file saving...')

        # save_content_to_csv(articles, day_string)
        articles.clear()

    url_2, search_date, new_date_format = load_next_day(soup, new_date_format)

'''
--- how to access dictionary:
retrieval_date = datetime.strptime('16. Oktober 2022', '%d. %B %Y').date()
print(all_article_links.get(retrieval_date))'''
