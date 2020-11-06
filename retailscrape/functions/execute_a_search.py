from classes.search_class import Search # type: ignore
from functions.helper_functions import setup_log # type: ignore
import time # type: ignore
from classes.outputdata_class import OutputData # type: ignore
from classes.product_class import Product # type: ignore # here for testing only
from classes.log_class import Log # type: ignore

def execute_a_search(search_term, scrape_log):
    # module_log = Log(module_name=scrape_log.module_name + 'execute_a_search')
    module_log = Log(module_name=scrape_log.module_name + f'.execute_a_search_{search_term}')
    module_log.log.info(f'starting a search')
    print('kkkkk')
    # Execute search
    search = Search(search_term, scrape_log)
    print('llllll')
    
    # (1) Set-up log
    # search.search_log = setup_log(search.search_log, search.search_term, search.search_log_level)
    # module_log.info(f'execute_a_search: Initiating new search for \'{search.search_term}\' on website {search.target_url} - max attempts limited to {search.max_get_attempts}')
    
    print('pppppp')
    search.testing = True
    if not search.testing:
        # (2) Open target website, submit search term, check searching for sub-category, get number of result page
        while search.open_website_unsuccessful or search.submit_unsuccessful or search.is_category_page or search.calc_num_result_pages_unsuccessful or search.page_processing_unsuccessful:
            
            # Increment attempt and check if max exceeded
            search.check_attempts()

            # Try to open website
            search.open_website()
        
            time.sleep(10)
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
            time.sleep(5)
            if not search.is_category_page:
                time.sleep(5)
                search.get_number_of_results_pages()
            
            # Test if calculated number of result pages
            if search.calc_num_result_pages_unsuccessful:
                module_log.log.info(f'execute_a_search: Search calc number pages unsuccessful - bool value={search.calc_num_result_pages_unsuccessful}')
                search.retry()

            #(6) Process and save the first page of results
            search.save_this_webpage_product_data()

            # (7) Process and save all subsequent result pages
            page_processing_unsuccessful = search.cycle_through_results_pages()
            if page_processing_unsuccessful:
                search.retry()
                get_attempts = search.get_attempts  # Save number of attempts
                search = Search(search_term) # Reset search instance as it maybe partially populated -
                search.get_attempts = get_attempts # Restore number of attempts
    else:
        # Create a couple of dummy products to test output process
        this_product = Product(0,0,'search_term','url', 'desc', 1.99, 2.99, 1.00, 'fulfillment', 'availability', '4')
        search.products.append(this_product)
        this_product = Product(0,1,'search for bob friend', 'test url other', 'product description new', 7.99, 9.99, 6.55, 'fulfillment new', 'availability yep', '5')
        search.products.append(this_product)

    # (8) 
    search.save_products()

    # (9) mark any products with duplicate descriptions
    search.flag_duplicate_products()

    # (10) Write data to results CSV
    # df = search.create_output()
    module_log.log.info(f'execute_a_search: Writing output file - {len(search.products)} product(s) created for search term \'{search.search_term}\'')
    # Output list of products
    sort_columns = ['SEARCH_TERM', 'RESULT_PAGE_NUMBER', 'RESULT_PAGE_INDEX_POSITION']
    search_output = OutputData(class_list=search.products, sort_columns=sort_columns, filename_term=search.search_term)
    search_output.save_list_as_df()
    search_output.save_df_as_csv()

    # (11) End
    module_log.log.info('End')
    search.end()
    return search_output.df, search.products