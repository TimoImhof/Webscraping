import time
import urllib.request, sys
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import os
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


def get_article_content_and_date(url):
    """ TODO: Takes a string (url) and extracts content and date from this url.
    Returns timestamp, headline and text of website."""
    soup = get_soup(url)
    timestamp = soup.find('span', attrs={'data-key': 'timestamp'})['title']
    headline_container = soup.find('div', attrs={'data-key': 'card-headline'})
    headline = headline_container.find('h1').text.strip()
    content = soup.find('div', attrs={'class': 'Article', 'data-key': 'article'})
    text = ''
    for phrase in content.find_all('p'):
        text = text + ' ' + phrase.text.strip()
    return timestamp, headline, text


def save_content_to_csv(content, date):
    """ Takes list of lists as content and string as date and writes content to new csv file named after string."""
    header = ['date', 'topline', 'headline', 'content']
    directory = 'C:\\Users\\Timo\\PycharmProjects\\Webscraping\\Tagesschau_archive\\'
    with open(file=directory + 'AP_News_' + date + '.csv', mode='x', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for article in content:
            writer.writerow([article[0], article[1], article[2], article[3]])


def update_csv(article, date):
    """ TODO: write  """
    directory = os.path.join('C:\\Users\\Timo\\PycharmProjects\\Webscraping\\AP_News_archive')
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('_AP_News.csv'):
                f = open((file, 'w'))
                # TODO: implement
                f.close()


def create_new_csv(header, date):
    """ TODO: implement """
    directory = 'C:\\Users\\Timo\\PycharmProjects\\Webscraping\\AP_News_archive\\'
    with open(file=directory + date + '_AP_News' + '.csv', mode='x', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)


soup = get_soup('https://apnews.com/hub/business?utm_source=apnewsnav&utm_medium=navigation')
links = get_links(soup)

for link in links:
    timestamp, headline, text = get_article_content_and_date(link)
    print(timestamp[0:16] + ' | ' + headline)
    try:
        update_csv([headline, text], timestamp[0:16])
    except Exception as e:
        print('No such file found. Create new one:')
        create_new_csv([timestamp[0:16], headline, text], timestamp[0:10])
