from pyramid.view import view_config


@view_config(
    route_name="dashboard/organizations",
    renderer="../templates/dashboard/organizations.mako",
)
def organizations(request):
    return {}
