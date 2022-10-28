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


def save_article_to_csv(timestamp, headline, text):
    """ TODO: write  """
    date = timestamp[0:10]
    time = timestamp[0:16]
    directory = os.path.join(os.getcwd() + '/AP_News_archive')  # get current directory
    csv_path = directory + '/' + date

    if not os.path.exists(csv_path):
        new_article_frame = pd.DataFrame({'time': time, 'headline': headline, 'text': text}, index=[0])
        new_article_frame.to_csv(csv_path, index=False, header=True)
        print('created new file for date: ' + date)
    else:
        print('file with date already exists...')
        old_article_frame = pd.read_csv(csv_path)
        latest_index = old_article_frame.index.values.max()
        if time in old_article_frame.get('time').values:
            print('article already contained in file...')
        else:
            print('append article to existing file...')
            new_row = pd.DataFrame([time, headline, text], index=[latest_index + 1])
            new_row.to_csv(csv_path, mode='a' , index=False, header = False)


soup = get_soup('https://apnews.com/hub/business?utm_source=apnewsnav&utm_medium=navigation')
links = get_links(soup)

for link in links:
    try:
        timestamp, headline, text = get_article_content_and_date(link)
        print(timestamp[0:16] + ' | ' + headline)
        save_article_to_csv(timestamp, headline, text)
    except Exception as e:
        print(str(e))
