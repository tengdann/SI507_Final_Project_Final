import unittest
from scraping import *
from database import *

# Testing takes awhile; opening up a Selenium window is an unintended side-effect of running scraping

class TestScraping(unittest.TestCase):
    def testUrl1(self):
        # This just scrapes, any formatting issues are handled by another function
        
        chromeOptions = webdriver.ChromeOptions()
        prefs = {'profile.managed_default_content_settings.images':2}
        chromeOptions.add_experimental_option("prefs", prefs)
        
        driver = webdriver.Chrome('./final_project/chromedriver-Windows', options = chromeOptions)
        
        conn = sqlite.connect(DBNAME)
        cur = conn.cursor()
    
        result = scrape_page(test_url1, driver, cur)
        self.assertEqual('By Zoe Kleinman', result[0]) # By is handled in another function
        self.assertEqual('4 December 2018', result[1])
        self.assertEqual('Unknown', result[2]) # May have unintended result
        self.assertEqual('Facebook', result[3]) # Page was updated, but old cached page had Bath as scraped tag
        driver.quit()
        
    def testUrl2(self):
        # This just scrapes, any formatting issues are handled by another function
        
        chromeOptions = webdriver.ChromeOptions()
        prefs = {'profile.managed_default_content_settings.images':2}
        chromeOptions.add_experimental_option("prefs", prefs)
        
        driver = webdriver.Chrome('./final_project/chromedriver-Windows', options = chromeOptions)
        
        conn = sqlite.connect(DBNAME)
        cur = conn.cursor()
    
        result = scrape_page(test_url2, driver, cur)
        self.assertEqual('BBC News', result[0]) # By is handled in another function
        self.assertEqual('4 December 2018', result[1])
        self.assertEqual('US & Canada', result[2]) # May have unintended result
        self.assertEqual('History', result[3]) # Page was updated, but old cached page had Bath as scraped tag
        driver.quit()
        
class TestDatabase(unittest.TestCase):
    def testArticles(self):
        conn = sqlite.connect(DBNAME)
        cur = conn.cursor()
        
        statement = '''
            SELECT title, date FROM Articles
        '''
        cur.execute(statement)
        results_list = cur.fetchall()
        self.assertTrue(len(results_list) > 0)
        conn.close()
        
    def testAuthors(self):
        conn = sqlite.connect(DBNAME)
        cur = conn.cursor()
        
        statement = '''
            SELECT author FROM Authors
        '''
        cur.execute(statement)
        results_list = cur.fetchall()
        self.assertTrue(len(results_list) > 0)
        self.assertIn(('BBC News',), results_list) # SQL is weird...
        self.assertIn(('Unknown',), results_list) # SQL is weird...
        conn.close()
        
    def testRegions(self):
        conn = sqlite.connect(DBNAME)
        cur = conn.cursor()
        
        statement = '''
            SELECT region FROM Regions
        '''
        cur.execute(statement)
        results_list = cur.fetchall()
        self.assertTrue(len(results_list) > 0)
        self.assertIn(('Unknown',), results_list) # SQL is weird...
        conn.close()
        
    def testTags(self):
        conn = sqlite.connect(DBNAME)
        cur = conn.cursor()
        
        statement = '''
            SELECT tag FROM Tags
        '''
        cur.execute(statement)
        results_list = cur.fetchall()
        self.assertTrue(len(results_list) > 0)
        self.assertIn(('Unknown',), results_list) # SQL is weird...
        conn.close()
        
        
def te_main():        
    unittest.main()
    
if __name__ == '__main__':
    te_main()