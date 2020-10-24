import time # type: ignore
from functions.execute_search import execute_search # type: ignore

def uber_search(search_terms):
    list_of_search_terms = search_terms.split(',') # Split search terms
   
    if len(list_of_search_terms) > 1: # If more than one iterate but return None
        success_message = 'Results: '
        for index, search_term in enumerate(list_of_search_terms):
            df = execute_search(search_term)
            success_message += f'({index+1}) {search_term}:{len(df)} products; '
            print('waiting')
            time.sleep(30)
        success_message += '\n' + 'To review results drag / drop CSVs found in the results folder (last search term results displayed below)'
        return df.to_dict(orient='records'), success_message
    
    else: # If only 1 search term execute search and return the single df
        df = execute_search(list_of_search_terms[0])
        success_message = f'...Search complete - found {len(df)} products for {list_of_search_terms[0]}'
        return df.to_dict(orient='records'), success_message