from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import re
import os
import sqlite3 as sqlite
from secrets import news_api_key
from database import DBNAME

api_key = news_api_key
api_baseurl = 'https://newsapi.org/v2/everything?'

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
# DEPENDENCIES: generate_url(), add_to_db()
def get_from_api(baseurl, params):
    pass
 
# REQUIRES: nothing
# MODIFIES: the DBNAME
# EFFECTS: adds information to the database
# DEPENDENCIES: nothing 
def add_to_db():
    pass

# REQUIRES: input is a dictionary for a single article
# MODIFIES: the DBNAME
# EFFECTS: adds information to the cache
# DEPENDENCIES: nothing
def selenium_cache(url):
    # Connect to the DBNAME
    conn = sqlite.connect(DBNAME)
    cur = conn.cursor()
    
    statement = '''
        SELECT EXISTS(SELECT 1 FROM Cache WHERE url = ?)
    '''
    cur.execute(statement, (url,))
    exists = cur.fetchone()
    
    if exists[0]:
        statement = '''
            SELECT html FROM Cache WHERE url = ?
        '''
        cur.execute(statement, (url,))
        html = cur.fetchone()[0]
    else:
        # Launch url
        driver = webdriver.Chrome('./final_project/chromedriver-Windows')
        driver.get(url)
        html = driver.page_source
        driver.quit()
        
        # Add to cache
        statement = '''
            INSERT INTO Cache (url, html) VALUES (?, ?)
        '''
        cur.execute(statement, (url, html))
        
    conn.commit()
    conn.close()    
    
    return html

# REQUIRES: url to an article
# MODIFIES: nothing
# EFFECTS: returns formatted information for db insertions
# DEPENDENCIES: selenium_cache
def scrape_page(url):  
    soup = BeautifulSoup(selenium_cache(url), 'html.parser')
    
    # Date published
    date = soup.find('div', {'class': 'date date--v2 relative-time'})['data-datetime']
    
    # Region
    region = soup.find('div', {'class': 'secondary-navigation secondary-navigation--wide'}).find('span').text
    
    # Find tags
    tags = []
    try:
        tags_temp = soup.find_all('li', {'class': 'tags-list__tags', 'data-entityid': 'topic_link_top'})
        for tag in tags_temp:
            tags.append(tag.find('a').text)
    except:
        pass
    
    return (date, region, tags)
    
scrape_page(test_url1)
scrape_page(test_url2)