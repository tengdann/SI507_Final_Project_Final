from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import json
from bs4 import BeautifulSoup
import re
import os
import sqlite3 as sqlite
import sys
from secrets import news_api_key
from database import DBNAME

sys.stdout.flush()

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
# DEPENDENCIES: generate_url(), add_to_db(), scrape_page
def get_from_api(baseurl, params):    
    # Selenium stuff
    # Don't load images?
    chromeOptions = webdriver.ChromeOptions()
    prefs = {'profile.managed_default_content_settings.images':2}
    chromeOptions.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome('./final_project/chromedriver-Windows', options = chromeOptions)
    
    # To prevent Selenium from stalling out occasionally
    driver.set_page_load_timeout(15)
    
    # SQLite stuff
    conn = sqlite.connect(DBNAME)
    cur = conn.cursor()
    
    articles = json.loads(requests.get(generate_url(baseurl, params)).text)

    for article in articles['articles']:
        # We only want news articles; sports pages are formatted differently
        # We also ignore videos, since Selenium might stall out while loading video
        if 'news' in article['url'] and 'av' not in article['url']:
            page_stuff = scrape_page(article['url'], driver, cur)              
            author = page_stuff[0].replace('By ', '')
            title = article['title']
            url = article['url']
            
            to_insert = (author, title, page_stuff[1], page_stuff[2], page_stuff[3], url)
            add_to_db(to_insert, cur)
            
            conn.commit()
        
    conn.close()
    driver.quit()
 
# REQUIRES: values is a valid tuple 
# MODIFIES: the DBNAME
# EFFECTS: adds information to the database
# DEPENDENCIES: nothing 
def add_to_db(values, cur):
    # Insert and get author_id
    statement = '''
        INSERT OR IGNORE INTO Authors (author) VALUES (?);
    '''
    cur.execute(statement, (values[0],))
    
    statement = '''
        SELECT id FROM Authors WHERE author = ?
    '''
    cur.execute(statement, (values[0],))
    author_id = cur.fetchone()[0]
    
    # Insert and get region_id
    statement = '''
        INSERT OR IGNORE INTO Regions (region) VALUES (?);
    '''
    cur.execute(statement, (values[3],))
    
    statement = '''
        SELECT id FROM Regions WHERE region = ?
    '''
    cur.execute(statement, (values[3],))
    region_id = cur.fetchone()[0]
    
    # Insert and get tag_id
    statement = '''
        INSERT OR IGNORE INTO Tags (tag) VALUES (?);
    '''
    cur.execute(statement, (values[4],))
    
    statement = '''
        SELECT id FROM Tags WHERE tag = ?
    '''
    cur.execute(statement, (values[4],))
    tag_id = cur.fetchone()[0]
    
    # Insert or replace into article
    # Since UPSERT isn't available for this SQLite3 version, gotta use this convoluted way
    statement = '''
        WITH new (author_id, title, [date], region_id, tag_id, url) AS ( VALUES(?, ?, ?, ?, ?, ?) )
            INSERT OR REPLACE INTO Articles (id, author_id, title, [date], region_id, tag_id, url)
            SELECT old.id, new.author_id, new.title, new.[date], new.region_id, new.tag_id, new.url
            FROM new LEFT JOIN Articles AS old ON new.title = old.title;
    '''
    cur.execute(statement, (author_id, values[1], values[2], region_id, tag_id, values[5]))

# REQUIRES: input is a dictionary for a single article
# MODIFIES: the DBNAME
# EFFECTS: adds information to the cache
# DEPENDENCIES: nothing
def selenium_cache(url, driver, cur):
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
        finished = 0
        while finished == 0:
            try:
                driver.get(url)
                finished = 1
            except:
                sleep(5)
        html = driver.page_source
        
        # Add to cache
        statement = '''
            INSERT INTO Cache (url, html) VALUES (?, ?)
        '''
        cur.execute(statement, (url, html))

    return html

# REQUIRES: url to an article
# MODIFIES: nothing
# EFFECTS: returns formatted information for db insertions
# DEPENDENCIES: selenium_cache
def scrape_page(url, driver, cur):  
    soup = BeautifulSoup(selenium_cache(url, driver, cur), 'html.parser')
    
    # Author?
    try:
        author = soup.find('div', {'class': 'byline'}).find('span', {'class': 'byline__name'}).text
    except:
        author = 'BBC News'
    
    # Date published
    try:
        date = soup.find('div', {'class': 'date date--v2 relative-time'})['data-datetime']
    except:
        date = 'Unknown'
    # HTML why
    if date is None:
        date = 'Unknown'
    
    # Region
    try:
        region = soup.find('div', {'class': 'secondary-navigation secondary-navigation--wide'}).find('span').text
    except:
        region = 'Unknown'
    # HTML why
    if region is None:
        region = 'Unknown'
    
    # Find tags
    try:
        tag = soup.find('li', {'class': 'tags-list__tags', 'data-entityid': 'topic_link_top'}).find('a').text
    except:
        try:
            tag = soup.find('li', {'class': 'tags-list__tags', 'data-entityid': 'topic_link_bottom'}).find('a').text
        except:
            tag = 'Unknown'
    # HTML why
    if tag is None:
        tag = 'Unknown'
    
    return (author, date, region, tag)
    
    
if __name__ == '__main__':
    print('WARNING: THIS WILL DO A NEW QUERY TO THE API')
    print('OTHERWISE THERE WOULD BE NO UPDATED STORIES')
    
    try:
        user_input = int(input('Please enter how many pages you would like to scrape: '))
    except:
        print('Error, you need to enter a number!')
        sys.exit(1)
        
    for i in range(1, user_input + 1):
        try:
            params = {'sources': 'bbc-news', 'apiKey': api_key, 'pageSize': '100', 'page': str(i)}
            get_from_api(api_baseurl, params)
            print('Data successfully scraped!', 'Page {} of {}'.format(i, user_input))
        except:
            print('Something went wrong; you\'ve probably reached the end of the API call!')
            sys.exit(1)