import time # type: ignore
import pandas as pd # type: ignore
from functions.execute_a_search import execute_a_search # type: ignore
from functions.helper_functions import create_log, log_remove_handlers
from classes.outputdata_class import OutputData # type: ignore
from classes.log_class import Log # type: ignore


def execute_all_searches(search_terms, scrape_log):
    execute_all_searches_log = Log(module_name=scrape_log.module_name + '.execute_all_searches')
    execute_all_searches_log.log.info(f'starting searches:search_terms={search_terms}')
    list_of_search_terms = search_terms.split(',') # Split search terms
    list_of_all_dfs = []
    list_all_product_class = []
    list_search_product_class = []

    if len(list_of_search_terms) > 1: # If more than one iterate but return None
        success_message = 'Results: '
        for index, search_term in enumerate(list_of_search_terms):
            df, list_search_product_class = execute_a_search(search_term, scrape_log)
            list_of_all_dfs.append(df)
            list_all_product_class.extend(list_search_product_class)
            success_message += f'({index+1}) {search_term}:{len(df)} products; '
            time.sleep(30)
        success_message += '\n' + 'To review results drag / drop CSVs found in the results folder - concatenated results displayed below'
    else: # If only 1 search term execute search and return the single df
        df, list_search_product_class = execute_a_search(list_of_search_terms[0], scrape_log)
        list_of_all_dfs.append(df)
        list_all_product_class.extend(list_search_product_class)
        success_message = f'...Search complete - found {len(df)} products for {list_of_search_terms[0]}. Results displayed below'
    all_dfs = pd.concat(list_of_all_dfs)
   
    # Output all products to csv
    sort_columns = ['SEARCH_TERM', 'RESULT_PAGE_NUMBER', 'RESULT_PAGE_INDEX_POSITION']
    search_output = OutputData(df=all_dfs, sort_columns=sort_columns, filename_term='all_products')
    search_output.save_df_as_csv()
    return all_dfs.to_dict(orient='records'), success_message, list_all_product_class