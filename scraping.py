from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import re
import os
import sqlite3 as sqlite
from secrets import news_api_key

api_key = news_api_key
api_baseurl = 'https://newsapi.org/v2/everything?'
DBNAME = 'final_project.sqlite'

test_url1 = 'https://www.bbc.com/news/uk-england-bristol-46420317'
test_url2 = 'https://www.bbc.com/news/world-us-canada-46421177'

# REQUIRES: api_baseurl is a valid API url, and params is a dictionary w/ valid key/value pairs for said API
# MODIFIES: nothing
# EFFECTS: returns url to be used for requests
# DEPENDENCIES: nothing
def generate_url(baseurl, params):
    url = baseurl
    for key in params:
        if key != list(params.keys())[-1]:
            url += key + '=' + params[key] + '&'
        else:
            url += key + '=' + params[key]
    
    return url

# REQUIRES: api_baseurl is a valid API url and params is a dictionary w/ valid key/value pairs for said API
# MODIFIES: the DBNAME
# EFFECTS: gets articles from specified website utilizing the cache
# DEPENDENCIES: generate_url(), add_to_cache()
def get_with_database(baseurl, params):
    pass

# REQUIRES: input is a dictionary for a single article
# MODIFIES: the DBNAME
# EFFECTS: adds information to the cache
# DEPENDENCIES: scrape_page()
def add_to_cache(input):
    pass

# REQUIRES: url to an article
# MODIFIES: nothing
# EFFECTS: returns formatted information for db insertions
# DEPENDENCIES: nothing
def scrape_page(url):
    # Launch url
    driver = webdriver.Chrome('./final_project/chromedriver-Windows')
    driver.get(url)
    
    # Pass-off to BeautifulSoup    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Date published
    date = soup.find('div', {'class': 'date date--v2 relative-time'})['data-datetime']
    print(date)
    
    # Region
    region = soup.find('div', {'class': 'secondary-navigation secondary-navigation--wide'}).find('span').text
    print(region)
    
    # Find tags
    tags = []
    tags_temp = soup.find_all('li', {'class': 'tags-list__tags', 'data-entityid': 'topic_link_bottom'})
    for tag in tags_temp:
        tags.append(tag.find('a').text)
    print(tags)

    driver.quit()