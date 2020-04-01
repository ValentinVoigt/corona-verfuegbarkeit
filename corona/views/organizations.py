from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from datetime import date
from wtforms import StringField, validators

import json

from ..models import Organization
from ..utils.form import Form


class OrganizationForm(Form):
    name = StringField("Name der Organisation", [validators.InputRequired()])
    city = StringField("Stadt")
    postal_code = StringField("Postleitzahl")


@view_config(
    route_name="dashboard/organizations",
    renderer="../templates/dashboard/organizations/list.mako",
    permission="loggedin",
)
def list(request):
    return dict(organizations=request.user.root_organizations)


@view_config(
    route_name="dashboard/organizations/show",
    renderer="../templates/dashboard/organizations/show.mako",
    permission="details",
)
def show(request):
    form = OrganizationForm(request.POST, request.context)
    if request.has_permission("edit"):
        if request.method == "POST" and form.validate():
            form.populate_obj(request.context)
            request.session.flash("Gespeichert.")

    return dict(organization=request.context, form=form)


@view_config(
    route_name="dashboard/organizations/new",
    renderer="../templates/dashboard/organizations/new.mako",
    permission="edit",
)
def new(request):
    form = OrganizationForm(request.POST)
    if request.method == "POST" and form.validate():
        organization = Organization(parent=request.context)
        form.populate_obj(organization)
        request.dbsession.add(organization)
        request.session.flash("Neue Organisation angelegt!")
        return HTTPFound(location=request.route_path("dashboard/organizations"))

    return dict(organization=request.context, form=form)


@view_config(
    route_name="dashboard/organizations/availability",
    renderer="../templates/dashboard/organizations/availability.mako",
    permission="details",
)
def availability(request):
    #datetime.datetime.strptime(date_string, format1).strftime(format2)

    data = {
        'type': 'bar',
        'data': {
            'labels': ["A", "B", "C"],
            'datasets': [
                {
                    'data': [10, 20, 30],
                    'backgroundColor': "blue",
                    'label': "asdf",
                },
                {
                    'data': [20, 30, 10],
                    'backgroundColor': "red",
                    'label': "roflcopter",
                },
            ],
        },
        'options': {
            'scales': {
                'yAxes': [{
                    'ticks': {
                        'beginAtZero': True,
                    },
                }],
            },
        },
    }
    return dict(organization=request.context, data=json.dumps(data))
