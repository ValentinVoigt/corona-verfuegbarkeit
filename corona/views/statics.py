from pyramid.view import view_config


@view_config(route_name="home", renderer="../templates/home.mako")
def home(request):
    return {}


@view_config(route_name="imprint", renderer="../templates/imprint.mako")
def imprint(request):
    return {}
