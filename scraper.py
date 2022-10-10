import binary as binary
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import chromedriver_autoinstaller


chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
                                      # then add chromedriver to path

# start browser session
driver = webdriver.Chrome()
driver.get("http://www.ryanhowerter.net/colors.php")

# extract content
content = driver.page_source
soup = BeautifulSoup(content)

for link in soup.find_all('a'):
    print(link.get('href'))

