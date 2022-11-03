import os
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_links(soup):
    """ Takes Beautifulsoup object, and returns list contaning all urls, which contain the substring 'article',
    to filter unnecessary urls. """
    links = []
    overview = soup.find('div', attrs={'class': 'Body'})
    for link in overview.find_all('a'):
        links.append('https://apnews.com' + link['href'])
    links = list(set(links))  # remove duplicates
    article_links = []
    for link in links:
        if 'article' in link:
            article_links.append(link)
    return article_links


def get_soup(url):
    """ Takes an url as string, sends a get request and returns a Beautifulsoup object from this url."""
    try:
        time.sleep(2)
        page = requests.get(url)
        return BeautifulSoup(page.text, 'html.parser')
    except Exception as e:
        print('Could not load page!')
        return -1


def get_article_content_and_date(url):
    """ Takes a string (url) and extracts and returns content and metadata."""
    soup = get_soup(url)
    timestamp = soup.find('span', attrs={'data-key': 'timestamp'})['title']
    headline = soup.find('div', attrs={'data-key': 'card-headline'}).find('h1').text.strip()
    content = soup.find('div', attrs={'class': 'Article', 'data-key': 'article'})
    text = ''
    for phrase in content.find_all('p'):
        text = text + ' ' + phrase.text.strip()
    return timestamp, headline, text


def save_article_to_csv(timestamp, headline, text):
    """ Save content to .csv file with rows timestamp, headline and text.
     Check if file already exists, if not create a new one with header and content as first column.
     Check if article already exists in existing file, if not only append content as new column."""
    time = timestamp[0:16]
    date = timestamp[0:10]
    directory = os.path.join(os.getcwd() + '/AP_News_archive')  # get current directory
    csv_path = directory + '/' + date

    if not os.path.exists(csv_path):
        new_article_frame = pd.DataFrame({'time': time, 'headline': headline, 'text': text}, index=[0])
        new_article_frame.to_csv(csv_path, index=False, header=True)
        print('created new file for date: ' + date)
    else:
        print('file with date already exists...')
        existing_csv = pd.read_csv(csv_path)
        if headline in existing_csv.get('headline').values:
            print('article already contained in file...')
        else:
            print('append article to existing file...')
            new_row = pd.DataFrame({'time': time, 'headline': headline, 'text': text}, index=[0])
            new_row.to_csv(csv_path, mode='a', index=False, header=False)


""" Retrieval session: """
soup = get_soup('https://apnews.com/hub/business?utm_source=apnewsnav&utm_medium=navigation')  # don't change this link
links = get_links(soup)

timedata = []

for link in links:
    try:
        timestamp, headline, text = get_article_content_and_date(link)
        print(timestamp[0:16] + ' | ' + headline)
        save_article_to_csv(timestamp, headline, text)
        timedata.append(timestamp[0:16])
    except Exception as e:
        print('Exception thrown:')
        print(str(e))
