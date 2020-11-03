import dash_html_components as html # type: ignore
import dash_bootstrap_components as dbc # type: ignore
import dash_core_components as dcc # type: ignore
import dash_table # type: ignore

def page_2_content():
    layout = html.Div(id='page_2_content', children=[html.Div(input()), html.Div(update_messages()), html.Div(detail())])
    return layout

def input():
    layout = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.H5('Drag and drop invoice line data set to display'), width='auto'
                    ),
                    dbc.Col(
                        [
                            dcc.Upload(
                            id='invoice_lines_upload_data',
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
                            html.Span(id='invoice_lines_output-data_upload'),
                        ], width='auto'
                    ),
                ], justify='start', align='center'  
            ),
            html.Hr(),
        ]
    )
    return layout

def update_messages():
    layout = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.H6(
                        className='text-primary',
                        id='invoice_lines_output_message_id'
                        ), width='12'
                    ),
                    dbc.Col(
                        html.H6(
                            className='text-success',
                        id='invoice_lines_output_success_id'
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
                    html.H3('Invoice Lines'), width={'size': 'auto', 'offset': 5}, 
                ),
            ),
            html.Hr(),
            dbc.Row(
                dash_table.DataTable(
                    id='invoice_line_table',
                    columns=[
                        {'name': 'Invoice #', 'id': 'INVOICE_NUMBER', 'hideable': True},
                        {'name': 'Invoice Date', 'id': 'INVOICE_DATE', 'hideable': True},
                        {'name': 'Product Name', 'id': 'INVOICE_LINE_PRODUCT_NAME', 'hideable': True},
                        {'name': 'Modified Product Description', 'id': 'INVOICE_LINE_PRODUCT_DESCRIPTION', 'hideable': True},
                        {'name': 'Product Description', 'id': 'description', 'hideable': True},
                        {'name': 'Web Selling Price', 'id': 'INVOICE_LINE_PRODUCT_WEB_SELLING_PRICE', 'hideable': True},
                        {'name': 'Calculated Cost Price', 'id': 'INVOICE_LINE_PRODUCT_CALCULATED_COST_PRICE', 'hideable': True},
                        {'name': 'Original Product Description', 'id': 'INVOICE_LINE_ORIGINAL_PRODUCT_DESCRIPTION', 'hideable': True},
                    ],
                    # style_cell={'textAlign': 'left'},
                    page_size=15,
                    style_data={'whiteSpace': 'normal', 'height': 'auto'},
                    style_cell={'maxWidth': '400px'},
                    style_as_list_view=True,
                    persistence=True,
                    persisted_props=['columns.name', 'data'],
                    persistence_type='session',
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