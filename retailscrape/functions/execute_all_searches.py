import time # type: ignore
from functions.execute_a_search import execute_a_search # type: ignore
from functions.helper_functions import create_log, log_remove_handlers, get_filename
import pandas as pd # type: ignore

def execute_all_searches(search_terms, DEBUG_LEVEL):
    list_of_search_terms = search_terms.split(',') # Split search terms
    list_of_result_dfs = []
    if len(list_of_search_terms) > 1: # If more than one iterate but return None
        success_message = 'Results: '
        for index, search_term in enumerate(list_of_search_terms):
            df = execute_a_search(search_term, DEBUG_LEVEL)
            list_of_result_dfs.append(df)
            success_message += f'({index+1}) {search_term}:{len(df)} products; '
            time.sleep(30)
        success_message += '\n' + 'To review results drag / drop CSVs found in the results folder - concatenated results displayed below'
        # return all_dfs.to_dict(orient='records'), success_message
    else: # If only 1 search term execute search and return the single df
        df = execute_a_search(list_of_search_terms[0], DEBUG_LEVEL)
        list_of_result_dfs.append(df)
        success_message = f'...Search complete - found {len(df)} products for {list_of_search_terms[0]}. Results displayed below'
        # return df.to_dict(orient='records'), success_message
    all_dfs = pd.concat(list_of_result_dfs)
    create_output_all(all_dfs)
    return all_dfs.to_dict(orient='records'), success_message
    
def create_output_all(all_dfs):
    all_dfs.sort_values(by=['search_term', 'result_page_number', 'result_page_index_position'],  inplace=True)
    results_filenpathandame = get_filename('all', typeoffile='results', suffix='.csv')
    all_dfs.to_csv(results_filenpathandame, sep='\t', index=False) 