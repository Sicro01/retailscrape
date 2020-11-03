import dash_html_components as html # type: ignore
import dash_core_components as dcc # type: ignore
import dash_bootstrap_components as dbc # type: ignore
import dash_table # type: ignore

def page_1_content():
    layout = html.Div(id='page_1_content', children=[html.Div(input()), html.Div(update_messages()), html.Div(detail())])
    return layout

def input(): 
    layout = dbc.Row(
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
                                id='results_upload_data',
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
                                multiple=True
                                ),
                                html.Span(id='results_output-data-upload'),
                            ], width='auto'
                        ),
                    ], justify='start', align='center'  
                ), html.Hr(),
    return layout

def update_messages():
    layout = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.H6(
                        className='text-primary',
                        id='results_output_message_id'
                        ), width='12'
                    ),
                    dbc.Col(
                        html.H6(
                            className='text-success',
                        id='results_output_success_id'
                        ), width='12'
                    ),
                ], 
            )
        ]
    )
    return layout

def detail():
    layout = html.Div(
        [
            dbc.Row(
                dbc.Col(
                    html.H3('Scrape Results'), width={'size': 'auto', 'offset': 5}, 
                ),
            ),
            html.Hr(),
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
                    # persistence=True,
                    # persisted_props=['columns.name', 'data'],
                    # persistence_type='session',
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
            )
        ]
    )
    return layout
    