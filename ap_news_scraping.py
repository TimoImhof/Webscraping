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
    directory = os.path.join(os.getcwd() + '/AP_News_archive')  # get current directory

    #article = {'timestamp': [timestamp[0:16]], 'headline': [headline], 'text': [text]}
    article_frame = pd.DataFrame({'headline': headline, 'text': text}, index = [timestamp[0:16]])
    csv_path = directory + '/' + date
    article_frame.to_csv(csv_path, mode='a', header=not os.path.exists(csv_path))
    '''
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('_Tagesschau.csv') and date in file:
                content = pd.read_csv(directory + '/' + file)
                print(content.date)
                df = pd.DataFrame['date', 'title', 'content']
                csv_path = directory + '/' + file
                df.to_csv(csv_path, mode='a', header=not os.path.exists(csv_path))'''




soup = get_soup('https://apnews.com/hub/business?utm_source=apnewsnav&utm_medium=navigation')
links = get_links(soup)

for link in links:
    timestamp, headline, text = get_article_content_and_date(link)
    print(timestamp[0:16] + ' | ' + headline)
    save_article_to_csv(timestamp, headline, text)
