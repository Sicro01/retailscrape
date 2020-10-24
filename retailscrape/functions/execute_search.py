from classes.search_class import Search # type: ignore
from functions.helper_functions import setup_log # type: ignore
import time # type: ignore

def execute_search(search_term):
    # Execute search
    search = Search(search_term)

    # (1) Set-up log
    search.search_log = setup_log(search.search_log, search.search_term, search.search_log_level)
    search.search_log.info(f'Search: Initiating new search for \'{search.search_term}\' on website {search.target_url} - max attempts limited to {search.max_get_attempts}')

    # (2) Open target website, submit search term, check searching for sub-category, get number of result page
    while search.open_website_unsuccessful or search.submit_unsuccessful or search.is_category_page or search.calc_num_result_pages_unsuccessful or search.page_processing_unsuccessful:
        
        # Increment attempt and check if max exceeded
        search.check_attempts()
        
        # Try to open website
        search.open_website()
        if not search.open_website_unsuccessful:
            time.sleep(5)
            search.submit_search_text()
        else:
            search.retry()
            continue # Restart loop
        
        # Try to submit search request
        if not search.submit_unsuccessful:
            time.sleep(5)
            search.check_if_category_page()
        else:
            search.retry()
            continue # Restart loop
        
        # Test if search term was a valid sub-category - if not a sub-category we will have aborted
        if not search.is_category_page:
            time.sleep(5)
            search.get_number_of_results_pages()
        
        # Test if calculated number of result pages
        if search.calc_num_result_pages_unsuccessful:
            search.retry()

        #(6) Process and save the first page of results
        search.save_this_webpage_product_data()

        # (7) Process and save all subsequent result pages
        page_processing_unsuccessful = search.cycle_through_results_pages()
        if page_processing_unsuccessful:
            get_attempts = search.get_attempts  # Save number of attempts
            search = Search(search_term) # Reset search instance as it maybe partially populated -
            search.get_appempts = get_attempts # Restore number of attempts
            search.retry()

    # (8) 
    search.save_products()

    # (9) mark any products with duplicate descriptions
    search.flag_duplicate_products()

    # (10) Write data to results CSV
    df = search.create_output()

    # (11) End
    search.search_log.info('End')
    search.end()
    return df