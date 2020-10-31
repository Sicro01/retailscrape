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
from functions.uber_search import uber_search # type: ignore

VALID_DEBUG_OPTIONS = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'] # List of valid debug levels
DEBUG_LEVEL = sys.argv[1] if (len(sys.argv) - 1) == 1 and sys.argv[1] in VALID_DEBUG_OPTIONS else 'INFO' # If argument entered set debug level

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], prevent_initial_callbacks=True)

body = html.Div(
    [
        dbc.Row(
                dbc.Col(
                    html.H3('Scrape Product Data From Walmart.com'), width={'size': 'auto', 'offset': 4},
                ),
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    html.H6('Enter product sub-category(s) (if multiple separate with a comma) to search for and click on search:'), width='3'
                ),
                dbc.Col(
                    dbc.Input(id='search_term_input', placeholder='e.g. coke', type='text'), width=3
                ),
                dbc.Col(
                    dbc.Button("Search", id='search_button', color='primary', className='m-1'), width='auto'
                ),
                dbc.Col(
                    html.H5('Or drag and drop an existing result set to display'), width='auto'
                ),
                 dbc.Col(
                     [
                        dcc.Upload(
                        id='upload_data',
                        children=html.Span([
                            'Drag and Drop or ',
                            html.A('Select Files')
                        ]),
                        style={
                            'width': '100%',
                            'height': '60px',
                            'lineHeight': '60px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                            'margin': '10px'
                        },
                        # Allow multiple files to be uploaded
                        multiple=False
                        ),
                        html.Span(id='output-data-upload'),
                     ], width='auto'
                ),
            ], justify='start', align='center'  
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    # html.H6('test'), width='12',
                    html.H6(
                       className='text-primary',
                       id='output_message_id'
                    ), width='12'
                ),
                dbc.Col(
                    # html.H6('Bob'), width='12'
                    html.H6(
                        className='text-success',
                     id='output_success_id'
                    ), width='12'
                ),
            ], 
        ),
        dbc.Row(
            dash_table.DataTable(
                id='result_table',
                columns=[
                    {'name': 'Results Page #', 'id': 'result_page_number', 'hideable': True},
                    {'name': 'Index Position on Page', 'id': 'result_page_index_position', 'hideable': True},
                    {'name': 'Search Term', 'id': 'search_term', 'hideable': True},
                    {'name': 'Source URL', 'id': 'url', 'hideable': True},
                    {'name': 'Product Description', 'id': 'description', 'hideable': True},
                    {'name': 'From Price', 'id': 'from_price', 'hideable': True},
                    {'name': 'To Price', 'id': 'to_price', 'hideable': True},
                    {'name': 'Fulfillment', 'id': 'fulfillment', 'hideable': True},
                    {'name': 'Availability', 'id': 'availability', 'hideable': True},
                    {'name': 'Star Rating', 'id': 'rating', 'hideable': True},
                    {'name': 'Duplicate Description?', 'id': 'duplicate_indicator', 'hideable': True},
                ],
                # style_cell={'textAlign': 'left'},
                page_size=15,
                style_data={'whiteSpace': 'normal', 'height': 'auto'},
                style_cell={'maxWidth': '400px'},
                style_as_list_view=True,
                style_data_conditional=[
                    {
                     'if': {'row_index': 'odd'},
                     'backgroundColor': 'rgb(248, 248, 248)'
                    }
                ],
                style_header={
                  'backgroundColor': 'rgb(230, 230, 230)',
                 'fontWeight': 'bold',
                 'textAlign': 'center'
                }
            ),
            className='pl-4'
        ),
    ],
    className='pl-4'
)

app.layout= html.Div([body])
# Execute Search
@app.callback(
    Output(component_id='result_table', component_property='data'),
    Output(component_id='output_success_id', component_property='children'),
    [Input(component_id='search_button', component_property='n_clicks')],
    [Input(component_id='upload_data', component_property='contents')],
    [State(component_id='upload_data', component_property='filename')],
    [State(component_id='search_term_input', component_property='value')]
)
def run_search(n_clicks, upload_contents, filename, search_terms):
    # Determine which input triggered the callback
    ctx = dash.callback_context
    if not ctx.triggered:
        input_id = 'No input yet'
    else:
        input_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Act on the trigger
    # User is trying to search
    if input_id == 'search_button':
        if search_terms != None: # Check search term entered
            print(f'run_search:{DEBUG_LEVEL}')
            tabledata, success_message = uber_search(search_terms, DEBUG_LEVEL)
            return tabledata, success_message
    # User is try to upload a result set
    if input_id == 'upload_data':
        content_type, content_string = upload_contents.split(',')
        decoded = (pybase64.standard_b64decode(content_string))
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        return df.to_dict(orient='records'), len(df)

# Return initial message
@app.callback(
    Output(component_id='output_message_id', component_property='children'),
    [Input(component_id='search_button', component_property='n_clicks')],
    [Input(component_id='upload_data', component_property='contents')],
    [State(component_id='upload_data', component_property='filename')],
    [State(component_id='search_term_input', component_property='value')]
)
def display_message(n_clicks, upload_contents, filename, search_terms):
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

    # User is try to upload a result set
    if input_id == 'upload_data':
        message = f'Uploading results filename \'{filename}\''
        return message

if __name__ == '__main__':
    app.run_server(debug=True)