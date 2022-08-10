# Utilities
import logging
import time
import os

# Webscraping 
from selenium import webdriver # !pip install selenium
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, InvalidArgumentException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager # !pip install webdriver_manager


def load_wiki_main_page(sleep_time=5):

    """
    Loads the home page from the Forgotten Realms Fandom Wiki.
    """
    
    # Silence webdriver download
    logging.getLogger('WDM').setLevel(logging.NOTSET)
    os.environ['WDM_LOG'] = 'False'

    # Define url and driver
    page_url = "https://forgottenrealms.fandom.com/wiki/"
    
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "profile.managed_default_content_settings.images": 2, # Optional - disables image loading
        'profile.managed_default_content_settings.javascript': 2 # Optional - disables Javascript
    } 
    
    chrome_options.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # Go to the wiki main page and wait for it to load
    driver.get(page_url)
    time.sleep(sleep_time)

    # Enable cookies (if necessary)
    try:
        driver.find_element(By.XPATH, '//div[text()="ACCEPT"]').click()
        
    except NoSuchElementException:
        pass
    
    return page_url, driver


def get_deity_url(in_list=list, verbose=False, sleep_time=5):
      
    """
    Collects data from the Forgotten Realms Fandom Wiki.

    Args: a list of pantheons to browse through.
     
    Returns: a nested dictionary providing for each pantheon, their deities and respective url.
    """
    
    out_dict = {}
                    
    #Define url and driver
    page_url, driver = load_wiki_main_page()


    # Go to the pantheon url and wait for the page to load
    for pantheon in in_list:
        
        out_dict[pantheon] = {}

        driver.get(page_url+'Category:'+pantheon)
        time.sleep(sleep_time)
    
        # Extract all found deities and their url
        target = driver.find_elements(By.CLASS_NAME, value="category-page__member-link")
    
        for deity in target:
            if 'Category:' not in deity.text: #skips the entries that are pantheons and not individual deities
                
                out_dict[pantheon].update({
                    deity.text : deity.get_attribute('href')
                })
                
                if verbose:
                    print('{} from {} successfully added'.format(deity.text, pantheon)) # Strip the 'Category:' prefix
                    
    return out_dict


def get_deity_details(in_dict:dict, verbose=False, sleep_time=5): 
    
    """
    Collects data from the Forgotten Realms Fandom Wiki.

    Args: dictionary of deity - url pairs as generated with the get_deity_url function.
     
    Returns:  a nested dictionary summarizing, for each deity, their alignment and domains.
    """

    out_dict = {}
    
    #Define url and driver
    page_url, driver = load_wiki_main_page()

    # Loop over deities to retrieve associated attributes:
    
    pantheons = list(in_dict.keys())
    
    for pantheon in pantheons:
        
        out_dict[pantheon] = {}
        
        for deity, deity_url in in_dict[pantheon].items():
            
            if verbose:
                print('Processing: {}'.format(deity))                   
    
            # Go to the deity page
            driver.get(deity_url)
            time.sleep(sleep_time)
        
            # Skip deities that are not referred to in 5E
            try:
                driver.find_element(By.XPATH,'//*[contains(@data-item-name, "edition5")]')
                                                           
            except NoSuchElementException:
                if verbose:
                    print("{} has no 5E tab".format(deity))
                continue
             
    
            try:
                # Extract attributes
                deity_alignment = driver.find_element(By.XPATH, 
                                                        '//*[contains(@data-source,"alignment5e")]/div'
                                                        ).text 
        
            except NoSuchElementException:
                deity_alignment = ''
                pass
    
            try:
    
                deity_domains = driver.find_element(By.XPATH,
                                                    '//*[contains(@data-source, "domains5e")]/div'
                                                    ).text.split(',\n')
        
            except NoSuchElementException:
                deity_domains = ''
                pass
                
        
            # Append attributes to the dictionary
            out_dict[pantheon].update({
                deity : {
                    'deity_alignment': deity_alignment,
                    'deity_domains' : deity_domains,
                }
            })
                            
    return out_dict


