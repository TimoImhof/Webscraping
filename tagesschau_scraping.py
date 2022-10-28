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
            print('new date is:')
            print(new_date)
            return create_new_link(new_date.date().year, new_date.date().month, new_date.date().day), new_date, True
        else:
            new_date = datetime.strptime(date_string, '%B %Y') + relativedelta(months=1)
            print('new date is:')
            print(new_date)
            return create_new_link(new_date.date().year, new_date.date().month), new_date, False

    except Exception as e:

        error_type, error_obj, error_info = sys.exc_info()
        print(error_obj)
        print('Date format has changed from "Month Year" to "Day. Month Year"!')
        new_date = datetime.strptime(date_string, '%d. %B %Y') + timedelta(days=1)
        return create_new_link(new_date.date().year, new_date.date().month, new_date.date().day), new_date, True


def extract_article_links(soup_object, url, index=2, more_articles=False):
    """ Takes Beautifulsoup object and extracts all article links on a webpage and returns them in a list."""
    first_page = soup_object.find_all('a', attrs={'class': 'teaser-xs__link'})
    links = []
    for article_links in first_page:
        links.append(article_links['href'])

    # too many articles for one page:
    more_pages = soup_object.find('ul', attrs={'class': 'paginierung__liste'})
    if more_pages.find('li', attrs={'class': 'next'}) is not None:
        if more_articles:
            next_page_url = url[:-1] + str(index)
        else:
            next_page_url = url + '&pageIndex=' + str(index)

        next_soup = get_soup(next_page_url)
        links.extend(extract_article_links(next_soup, next_page_url, index + 1, True))
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


def retrieve_article_content(soup_object):
    """ Takes an Beautifulsoup object and returns all written text as one string"""
    article = soup_object.find('article', attrs={'class': 'container content-wrapper__group'})
    date = article.find('div', attrs={'class': 'metatextline'}).text.strip()
    topline = article.find('span', attrs={'class': 'seitenkopf__topline'}).text.strip()
    headline = article.find('span', attrs={'class': 'seitenkopf__headline--text'}).text.strip()
    text = ''
    for para in article.find_all('p', attrs={'class': 'm-ten m-offset-one l-eight l-offset-two textabsatz columns '
                                                      'twelve'}):
        text = text + para.text.strip() + ' '
    print(date[7:] + ': ' + topline + ' | ' + headline)
    return date[7:], topline, headline, text


def save_content_to_csv(content, date):
    """ Takes list of lists as content and string as date and writes content to new csv file named after string."""
    header = ['date', 'topline', 'headline', 'content']
    directory = 'C:\\Users\\Timo\\PycharmProjects\\Webscraping\\Tagesschau_archive\\'
    with open(file=directory + date + '_Tagesschau' + '.csv', mode='x', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for article in content:
            writer.writerow([article[0], article[1], article[2], article[3]])


def has_results(soup_object):
    """ Takes Beautifulsoup object and extracts number of article links.
    Returns False if there are no links, otherwise True."""
    numb_results = soup_object.find('span', attrs={'class': 'ergebnisse__anzahl'}).text.strip()
    return int(numb_results) != 0


'''--- Retrieval Session ---'''

locale.setlocale(locale.LC_TIME, "de_DE")

url_1 = 'https://www.tagesschau.de/archiv/'
url_2 = '?datum=2022-01-01'
start_time_index = datetime.strptime('1. Januar 2022', '%d. %B %Y')
end_time_index = datetime.strptime('27. Oktober 2022', '%d. %B %Y')

is_new_date_format = False
article_links = []

'retrieve all article links: '

while start_time_index.date() != end_time_index.date():
    soup = get_soup(url_1 + url_2)
    # print("loaded archive page...")

    if soup != -1 and has_results(soup):
        articles = []
        article_links = extract_article_links(soup, url_1 + url_2)
        # print('got all article links...')
        day_string = start_time_index.date().strftime('%Y-%m-%d')

        print('start extracting content from links...')
        for link in article_links:
            link_soup = get_soup(link)
            if link_soup != -1:
                try:
                    date, topline, headline, content = retrieve_article_content(link_soup)
                    articles.append([date, topline, headline, content])
                except Exception as e:
                    print(
                        'Could not extract article with standard pattern.')
        print('finished extraction... \nproceed to file saving...')

        save_content_to_csv(articles, day_string)
        articles.clear()

    url_2, start_time_index, is_new_date_format = load_next_day(soup, is_new_date_format)
