from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from wtforms import StringField, BooleanField, validators

from ..utils.form import Form
from ..models import Status


class StatusForm(Form):
    name = StringField("Name", [validators.InputRequired()])
    color = StringField("Farbe", [validators.InputRequired()])
    is_available = BooleanField("Gilt als verfügbar")


@view_config(
    route_name="dashboard/status/show",
    renderer="../templates/dashboard/organizations/statuses/show.mako",
)
def show(request):
    form = StatusForm(request.POST, request.context)
    if request.method == "POST" and form.validate():
        form.populate_obj(request.context)
        request.session.flash("Gespeichert.")
    return dict(status=request.context, form=form)


@view_config(
    route_name="dashboard/status/new",
    renderer="../templates/dashboard/organizations/statuses/new.mako",
    permission="edit",
)
def new(request):
    form = StatusForm(request.POST)
    if request.method == "POST" and form.validate():
        role = Status(organization=request.context)
        form.populate_obj(role)
        request.session.flash("Gespeichert.")
        return HTTPFound(
            location=request.route_path(
                "dashboard/organizations/show", id=request.context.id
            )
        )

    return dict(organization=request.context, form=form)
