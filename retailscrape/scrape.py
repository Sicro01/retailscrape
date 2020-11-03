import pybase64 # type: ignore
import io # type: ignore
import sys # type: ignore
import dash # type: ignore
from dash.dependencies import Input, Output, State # type: ignore
import dash_table # type: ignore
import dash_bootstrap_components as dbc # type: ignore
import dash_core_components as dcc # type: ignore
import dash_html_components as html # type: ignore
import pandas as pd # type: ignore
import time # type: ignore

# Local modules
from functions.execute_all_searches import execute_all_searches # type: ignore
from page_parts.location  import location # type: ignore
from page_parts.navbar import navbar # type: ignore
from page_parts.output import output # type: ignore
from page_parts.page_1_content import page_1_content # type: ignore
from page_parts.page_2_content import page_2_content # type: ignore 

VALID_DEBUG_OPTIONS = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'] # List of valid debug levels
DEBUG_LEVEL = sys.argv[1] if (len(sys.argv) - 1) == 1 and sys.argv[1] in VALID_DEBUG_OPTIONS else 'INFO' # If argument entered set debug level

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], prevent_initial_callbacks=True)

app.layout = dbc.Container(fluid=True, className='m-0, p-0', children=[location(), navbar(), output()])

# Display page html
@app.callback(
    Output('page_content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(url):
    if url in ('/', '/page-1'):
        return page_1_content()
    elif url == '/page-2':
        return page_2_content()
    else:
        print('else')
        return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {url} was not recognised..."),
        ]
    )

# Execute Search and re-display page links
@app.callback(
    Output(component_id='result_table', component_property='data'),
    Output(component_id='results_output_success_id', component_property='children'),
    [Input(component_id='search_button', component_property='n_clicks')],
    [Input(component_id='results_upload_data', component_property='contents')],
    [State(component_id='results_upload_data', component_property='filename')],
    [State(component_id='search_term_input', component_property='value')]
)
def run_search(n_clicks, upload_contents, filename, search_terms):
    # Determine which input triggered the callback
    ctx = dash.callback_context
    if not ctx.triggered:
        input_id = 'No input yet'
    else:
        input_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # User is trying to search
    if input_id == 'search_button':
        if search_terms != None: # Check search term entered
            tabledata, success_message = execute_all_searches(search_terms, DEBUG_LEVEL)
            return tabledata, success_message

    # User is try to upload a result set
    if input_id == 'results_upload_data':
        if upload_contents is not None:
            list_df_all = []
            success_message = 'Uploaded: '
            for upload, this_filename in zip(upload_contents, filename):
                df = parse_uploaded_results(upload)
                list_df_all.append(df)
                success_message += f'File: {this_filename}({len(df)} rows); '
            df_all = pd.concat(list_df_all)
        return df_all.to_dict(orient='records'), success_message

def parse_uploaded_results(upload):
    content_type, content_string = upload.split(',')
    decoded = (pybase64.standard_b64decode(content_string))
    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), sep='\t')
    return df

# Return initial message
@app.callback(
    Output(component_id='results_output_message_id', component_property='children'),
    [Input(component_id='search_button', component_property='n_clicks')],
    [State(component_id='search_term_input', component_property='value')]
)
def display_message(n_clicks, search_terms):
    # Determine which input triggered the callback
    ctx = dash.callback_context
    if not ctx.triggered:
        input_id = 'No input yet'
    else:
        input_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # User is trying to search
    if input_id == 'search_button':
        if search_terms != None:
            list_of_search_terms = search_terms.split(',')
            if len(list_of_search_terms) > 1:
                start_message = 'Multiple search terms entered; Once searches are complete review results using drag and drop feature. Searching for product sub-categories:'
                for index, search_term in enumerate(list_of_search_terms):
                    start_message += f'({index+1}) {search_term}; '
                return start_message
            else: 
                start_message = f'Single search term entered - searching for product sub-category...'
                start_message += f'\'{list_of_search_terms[0]}\''
                start_message += ' - results will be displayed below'
                return start_message
        else:
            return 'Please enter one or more product sub-categories'

# Display Invoice Lines
@app.callback(
    Output(component_id='invoice_line_table', component_property='data'),
    Output(component_id='invoice_lines_output_success_id', component_property='children'),
    [Input(component_id='invoice_lines_upload_data', component_property='contents')],
    [State(component_id='invoice_lines_upload_data', component_property='filename')],
)
def display_invoice_lines(upload_contents, filename):
    if upload_contents is not None:
        list_df_all = []
        success_message = 'Uploaded: '
        for upload, this_filename in zip(upload_contents, filename):
            df = parse_uploaded_invoice_lines(upload)
            list_df_all.append(df)
            success_message += f'File: {this_filename}({len(df)} rows); '
        df_all = pd.concat(list_df_all)
        return df_all.to_dict(orient='records'), success_message

def parse_uploaded_invoice_lines(upload):
    print(type(upload))
    content_type, content_string = upload.split(',')
    decoded = (pybase64.standard_b64decode(content_string))
    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), sep=',')
    return df

if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_ui=False, dev_tools_props_check=False)