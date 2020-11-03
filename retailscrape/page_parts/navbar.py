import dash_bootstrap_components as dbc # type: ignore
import dash_html_components as html # type: ignore
# DSLOGO = 'C:\\Users\\simon\\Documents\\py_projects\\retailscrape\\retailscrape\\images\\dslogo.png'

def navbar():
    layout = html.Div( 
        [
            dbc.Row(
                [
                    dbc.Col(
                            dbc.NavbarSimple(
                            children=[
                                dbc.NavItem(dbc.NavLink("Scrape", href='/page-1'), id='page_1_link'),
                                dbc.NavItem(dbc.NavLink("Review Invoice Lines", href='/page-2'), id='page_2_link'),
                            ],
                            brand='Walmart Invoice Margin Error Detection',
                            brand_href="#",
                            color="dark",
                            dark=True,
                        )
                    )
                ],
            ),
        ]
    )
    return layout