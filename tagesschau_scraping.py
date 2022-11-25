import locale
import os
import sys
import time
from datetime import datetime, timedelta

import pandas as pd
import requests
from bs4 import BeautifulSoup


def create_new_link(year, month, day=None):
    """ Create new URL by inserting parameters in URL format"""
    if day is None:
        return '?datum=' + str(year) + '-' + str(month).zfill(2) + '-01'
    else:
        return '?datum=' + str(year) + '-' + str(month).zfill(2) + '-' + str(day).zfill(2)


def load_next_page(soup_object, is_new_format):
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
            new_date = datetime.strptime(date_string, '%B %Y') + timedelta(months=1)
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
    return date[7:23], topline, headline, text


def save_article_to_csv(date_filename, article):
    """ Save content to .csv file with rows timestamp, headline and text.
     Check if file already exists, if not create a new one with header and content as first column.
     Check if article already exists in existing file, if not only append content as new column."""

    directory = os.path.join(os.getcwd(), 'Tagesschau_archive')  # get current directory
    check_for_directory(directory)
    csv_path = os.path.join(directory, date_filename)

    if not os.path.exists(csv_path):
        new_article_frame = pd.DataFrame(
            {'date': article[0], 'topline': article[1], 'headline': article[2], 'text': article[3]},
            index=[0])
        new_article_frame.to_csv(csv_path, index=False, header=True)
        print('created new file for date: ' + date_filename)
    else:
        print('file with date already exists...')
        existing_csv = pd.read_csv(csv_path)
        if article[2] in existing_csv.get('headline').values:
            print('article already contained in file...')
        else:
            print('append article to existing file...')
            new_row = pd.DataFrame(
                {'date': article[0], 'topline': article[1], 'headline': article[2], 'text': article[3]},
                index=[0])
            new_row.to_csv(csv_path, mode='a', index=False, header=False)


def has_results(soup_object):
    """ Takes Beautifulsoup object and extracts number of article links.
    Returns False if there are no links, otherwise True."""
    numb_results = soup_object.find('span', attrs={'class': 'ergebnisse__anzahl'}).text.strip()
    return int(numb_results) != 0


def check_for_directory(path):
    """ Check if directory specified by parameter path already exists, if not create it."""
    if not os.path.exists(path):
        os.mkdir(path)


def start_retrieval(date=datetime.today().strftime('%Y-%m-%d'), make_full_retrieval=False):
    """ TODO """
    locale.setlocale(locale.LC_TIME, "de_DE.utf8")  # important for datetime library because of "Januar" != "January"
    url_1 = 'https://www.tagesschau.de/archiv/'
    if make_full_retrieval:
        url_2 = '?datum=2010-01-01'
    else:
        url_2 = '?datum=' + date
    current = datetime.strptime(date, '%Y-%m-%d')
    latest = datetime.today() + timedelta(days=1)
    is_new_date_format = False
    directory = os.path.join(os.getcwd(), 'Tagesschau_archive')  # build path were to save extracted data
    check_for_directory(directory)  # check if directory already exists
    while current.date() != latest.date():
        print(f'Current date= {current.date()}')
        soup = get_soup(url_1 + url_2)  # get content of archive page listing all articles
        if soup != -1 and has_results(soup):  # if month or day has no articles proceed with next one
            article_links = extract_article_links(soup, url_1 + url_2)
            print('successfully loaded archive page and extracted article links...')
            date_filename = current.date().strftime('%Y-%m-%d')
            print('start extracting content from links...')
            for link in article_links:  # for each article extract date, topline, headline and content and save to csv
                link_soup = get_soup(link)
                if link_soup != -1:
                    try:
                        content = retrieve_article_content(link_soup)
                        save_article_to_csv(date_filename, content)
                    except Exception as e:
                        print(
                            'Could not extract article with standard pattern.\n Proceed with next one...')
            print('finished extraction and content saving...')
        url_2, current, is_new_date_format = load_next_page(soup, is_new_date_format)
