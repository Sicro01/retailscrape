import dash_html_components as html # type: ignore
import dash_bootstrap_components as dbc # type: ignore

def title():
    layout = html.Div([
        dbc.Row(
                dbc.Col(
                    html.H3('Scrape Product Data From Walmart.com'), width={'size': 'auto', 'offset': 4}, 
                ),
            ),
        html.Hr()
    ])
    return layout