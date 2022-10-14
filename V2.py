import urllib.request, sys, time
from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt


# guide: https://towardsdatascience.com/scraping-1000s-of-news-articles-using-10-simple-steps-d57636a49755

# url of the page that we want to Scarpe
# +str() is used to convert int datatype of the page no. and concatenate that to a URL for pagination purposes.
url = 'https://www.politifact.com/factchecks/list/?page=' + str(1)
# Use the browser to get the URL. This is a suspicious command that might blow up.

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

upperframe = []
frame = []

links = soup.find_all('li', attrs={'class': 'o-listicle__item'})
for j in links:
    statement = j.find("div", attrs={'class': 'm-statement__quote'}).text.strip()
    link = j.find("div", attrs={'class': 'm-statement__quote'}).find('a')['href'].strip()
    date_and_author = j.find('footer', attrs={'class': 'm-statement__footer'}).text[-17:-1].strip()
    title = j.find('div', attrs={'class': 'm-statement__author'}).find('a').get('title').strip()
    frame.append([statement, link, date_and_author, title])
    upperframe.extend(frame)

#print(upperframe)

data = pd.DataFrame(upperframe, columns=['statement', 'link', 'date_and_author', 'title'])
print(data['title'])
data.plot(x = 'statement', y = 'date_and_author', kind = 'scatter')
plt.show()

filename = "Example.csv"
f = open(filename,'w')
headers = 'Statement, Link, Date, Source, Label\n'
f.write(headers)
f.close()