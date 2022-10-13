import html
import re

import binary as binary
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import chromedriver_autoinstaller

# Check if the current version of chromedriver exists
# and if it doesn't exist, download it automatically,
# then add chromedriver to path
chromedriver_autoinstaller.install()

# start browser session
driver = webdriver.Chrome()
driver.get("http://www.ryanhowerter.net/colors.php")

# extract webpage content
content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')  # use standard python html parser

# divide page in head and body
head_tag = soup.head
body_tag = soup.body

colour_table = []
table = body_tag.find_all(class_='right legoname')
for child in table:
    colour_table.append(child['style'].split()[3])

final = colour_table.copy()
final = list(set(final)) # remove duplicates

print(len(colour_table))
print(len(final))





