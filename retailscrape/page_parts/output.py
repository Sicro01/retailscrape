import dash_html_components as html # type: ignore
import dash_core_components as dcc # type: ignore

def output():
    layout = html.Div(id='page_content')
    return layout