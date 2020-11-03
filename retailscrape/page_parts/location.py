import dash_core_components as dcc # type: ignore

def location():
    layout = dcc.Location(id='url', refresh=False)
    return layout