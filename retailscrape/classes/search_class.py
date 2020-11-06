from bs4 import BeautifulSoup as bsoup # type: ignore
from selenium.common.exceptions import TimeoutException, NoSuchAttributeException # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
from webdriver_manager.chrome import ChromeDriverManager # type: ignore
from pathlib import Path # type: ignore
from selenium.webdriver.common.by import By # type: ignore
import collections # type: ignore
import time # type: ignore
from typing import List, Set, Dict, Tuple, Optional # type: ignore
from functions.helper_functions import create_log, log_remove_handlers
from classes.driver_class import Driver # type: ignore
from classes.webpage_class import Webpage # type: ignore
from classes.product_class import Product # type: ignore
import pandas as pd # type: ignore
from classes.log_class import Log # type: ignore

class Search:
    def __init__(self, search_term='coke', scrape_log=''):
        self.chrome_driver = ''
        self.search_input_id = 'global-search-input'
        self.search_input_selector = (By.ID, self.search_input_id)
        self.search_term = search_term
        self.webpages = []
        self.current_result_page_number = 1
        self.products = []
        self.number_of_result_pages = 0
        self.page_range_cssclass = 'paginator-list'
        self.get_attempts = 0
        self.max_get_attempts = 3
        self.target_url = 'https://www.walmart.com/'
        self.target_url_search = self.target_url + '/search/?query=' + self.search_term
        self.search_execution_failed = True
        self.not_got_target_url = True
        self.module_log = Log(module_name=scrape_log.module_name + f'.search.{self.search_term}')
        self.target_url_soup = None
        self.first_page_soup = None
        self.open_website_unsuccessful = True
        self.submit_unsuccessful = True
        self.is_category_page = True
        self.calc_num_result_pages_unsuccessful = True
        self.page_processing_unsuccessful = True
        self.next_page_xpath = "//button[contains(@class, 'paginator-btn-next')]"
        self.next_page_selector = (By.XPATH, self.next_page_xpath)
        self.testing = False
        
    def retry(self):
        self.module_log.log.info(f'retry: Retrying - current attempt # {self.get_attempts}')
        self.chrome_driver.driver.close()
        time.sleep(5)
        
    def check_attempts(self):
        self.get_attempts += 1
        if self.get_attempts > self.max_get_attempts:
            self.module_log.log.critical(f'check_attempts: Critical Error: Exceeded number of re-try attempts {self.get_attempts} to search for {self.search_term}')
            self.abort()
    
    def end(self):
        try:         
            self.chrome_driver.driver.close() 
        except Exception as ex:
            pass
        
    def abort(self):
        try:
            self.module_log.log.critical(f'abort: Aborting search - trying to close log and Chrome')
            log_remove_handlers(self.module_log)
            self.chrome_driver.driver.close()
            quit()
        except Exception as ex:
            self.module_log.log.critical(f'abort: Aborting failed')
            self.module_log.log.critical(f'abort: Error details:{ex}:')
        quit()
        
    def open_website(self):
        self.module_log.log.info(f'open_website: Opening website and searching {self.target_url_search} - attempt # {self.get_attempts}')
        #Fire up Chrome and try to go to target website
        self.chrome_driver = Driver()
        self.chrome_driver.driver.get(self.target_url_search) # Open Chrome and access target website

        # Test if we've got the target url
        self.open_website_unsuccessful = True if self.chrome_driver.driver.current_url != self.target_url_search else False
        self.target_url_soup = bsoup(self.chrome_driver.driver.page_source, 'html.parser')

        # Return success / fail response
        if not self.open_website_unsuccessful:
            self.module_log.log.info(f'open_website: Successfully opened {self.target_url} searching for {self.search_term}')
        else:
            self.module_log.log.warning(f'open_website: Error: Unable to open {self.target_url_search}')
        return self.open_website_unsuccessful
    
    def submit_search_text(self):
        self.module_log.log.info(f'submit_search_text: Submitting search for \'{self.search_term}\'')
        try:
            search_input = self.chrome_driver.wait.until(EC.element_to_be_clickable(self.search_input_selector)) # Find the text box to enter search term
            # search_input.clear() # Clear any previous text entries
            # search_input.send_keys(self.search_term) # Submit search term
            search_input.submit() # 'Press enter' and trigger search
            self.first_page_soup = bsoup(self.chrome_driver.driver.page_source, 'html.parser')
            self.submit_unsuccessful = False
            self.module_log.log.debug(f'submit_search_text: Searching for \'{self.search_term}\' successful')
        except TimeoutException as ex:
            self.module_log.log.warning(f'submit_search_text: Warning: Timeout Exception trying to search for {self.search_term}')
            self.module_log.log.warning(f'submit_search_text: Error details:{ex}:')
            self.submit_unsuccessful = True
        return self.submit_unsuccessful
    
    def check_if_category_page(self):
        self.module_log.log.info(f'check_if_category_page: Checking if search item \'{self.search_term}\' is a sub-category')
        self.is_category_page = self.first_page_soup.find('div', class_='CategoryApp')
        self.is_category_page = True if self.is_category_page else False
        if self.is_category_page:
            self.module_log.log.warning(f'check_if_category_page: User Error: Search term \'{self.search_term}\' is a major category; re-submit search using a sub-category.')
        else:
            self.module_log.log.info(f'check_if_category_page: Category Page check for \'{self.search_term}\' successful')
        return self.is_category_page

    def get_number_of_results_pages(self):
        self.module_log.log.info(f'get_number_of_results_pages: Finding number of result pages for \'{self.search_term}\'')
        # self.calc_num_result_pages_unsuccessful = self.calc_number_of_result_pages()
        self.calc_number_of_result_pages()
        if self.calc_num_result_pages_unsuccessful:
            self.module_log.log.warning(f'get_number_of_results_pages: Warning: Exception trying to calculate number of pages')    
        else:
            self.module_log.log.info(f'get_number_of_results_pages: Found {self.number_of_result_pages} results pages for \'{self.search_term}\'')
        # return self.calc_num_result_pages_unsuccessful

    def calc_number_of_result_pages(self):
        try:
            page_range = self.first_page_soup.find('ul', class_= self.page_range_cssclass).li.a['aria-label']
            from_to_page_range = [int(i) for i in page_range.split() if i.isdigit()]
            self.number_of_result_pages = from_to_page_range[1]
            self.calc_num_result_pages_unsuccessful = False
            self.module_log.log.debug(f'calc_number_of_result_pages: Successful:{self.number_of_result_pages}')
        except Exception as ex:
            self.module_log.log.warning(f'calc_number_of_result_pages: Warning: Exception trying to calculate number of pages')
            self.module_log.log.warning(f'Exception:{ex}')
            self.calc_num_result_pages_unsuccessful = True
        # return self.calc_num_result_pages_unsuccessful
    
    def cycle_through_results_pages(self):
        try:
            for page in range(self.number_of_result_pages - 1):
                time.sleep(5)
                self.click_next() # Click to display next results webpage
                self.save_this_webpage_product_data() # Capture this webpage's html
                self.page_processing_unsuccessful = False
        except Exception as ex:
            self.page_processing_unsuccessful = True
            self.module_log.log.warning(f'cycle_through_results_pages: Warning: Exception trying to cycle through pages.  Search for {self.search_term} will be re-started')
            self.module_log.log.warning(f'Exception:{ex}')
        return self.page_processing_unsuccessful
    
    def click_next(self):
        next_page_button = self.chrome_driver.wait.until(EC.element_to_be_clickable(self.next_page_selector))
        next_page_button.click()
        time.sleep(3)
    
    def save_this_webpage_product_data(self):
        self.module_log.log.info(f'save_this_webpage_product_data: Capturing data - page {self.current_result_page_number} of {self.number_of_result_pages}')
        soup = bsoup(self.chrome_driver.driver.page_source, 'html.parser')
        webpage = Webpage(soup, self.chrome_driver.driver.current_url, self.current_result_page_number)
        webpage.get_product_data(self.search_term)
        self.webpages.append(webpage)
        self.module_log.log.info(f'save_this_webpage_product_data:Captured data page:{self.current_result_page_number} of {self.number_of_result_pages}')
        self.current_result_page_number += 1
    
    def save_products(self):
        self.module_log.log.info('save_products: concat products')
        for webpage_index, webpage in enumerate(self.webpages):
            self.module_log.log.debug(f'save_search_results: Saving webpage:{webpage_index}')
            self.products = self.products + webpage.products
        self.module_log.log.debug(f'save_search_results: len(self.products): {len(self.products)}')
    
    def flag_duplicate_products(self):
        self.module_log.log.info('flag_duplicate_products: Flagging duplicates')
        all_product_descriptions = [product.description for product in self.products]
        duplicate_product_descriptions = [item for item, count in collections.Counter(all_product_descriptions).items() if count > 1] # Create list of descriptions which appear > 1
        all_products_set = set(self.products)
        duplicate_products_set = set([product for product in self.products if product.description in duplicate_product_descriptions]) # Create list of products with duplicate descriptions
        [Product.set_duplicate(product) for product in list(duplicate_products_set)] # Set the duplicate indicator to Y for all products with a duplicate description
        unique_products_set = all_products_set.difference(duplicate_products_set) # Get the differences between the duplicate products and all products to identify the unique products
        self.products = list(duplicate_products_set) + list(unique_products_set) # Combine unique and duplicate sets
        self.module_log.log.debug(f'flag_duplicate_products:len(self.products):{len(self.products)}')
