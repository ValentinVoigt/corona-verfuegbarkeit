from pyramid.httpexceptions import HTTPFound, HTTPNotFound
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
    try:
        mydate = date(*[int(i) for i in request.matchdict["date"].split("-")])
    except:
        raise HTTPNotFound()

    roles = [
        {
            "label": "Alle",
            "day": request.context.num_available(mydate, "day"),
            "night": request.context.num_available(mydate, "night"),
        }
    ] + [
        {
            "label": r.name,
            "day": request.context.num_available(mydate, "day", r),
            "night": request.context.num_available(mydate, "night", r),
        }
        for o, r in request.context.recursive_roles
    ]

    data = {
        "type": "bar",
        "data": {
            "labels": [r["label"] for r in roles],
            "datasets": [
                {
                    "data": [r["day"] for r in roles],
                    "backgroundColor": "#EF810E",
                    "label": "Tagsüber",
                },
                {
                    "data": [r["night"] for r in roles],
                    "backgroundColor": "#001A26",
                    "label": "Nachts",
                },
            ],
        },
        "options": {"scales": {"yAxes": [{"ticks": {"beginAtZero": True}}]}},
    }

    return dict(organization=request.context, data=json.dumps(data), mydate=mydate)
