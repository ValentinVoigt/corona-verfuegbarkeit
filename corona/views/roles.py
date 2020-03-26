from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from wtforms import StringField, IntegerField, validators, ValidationError

from ..utils.form import Form
from ..models import Role


class RoleForm(Form):
    name = StringField("Name", [validators.InputRequired()])
    color = StringField("Farbe", [validators.InputRequired()])
    minimum_required = IntegerField(
        "Minimale Anzahl Mitglieder", [validators.optional()]
    )

    def validate_minimum_required(form, field):
        if type(field.data) is int and field.data < 0:
            raise ValidationError("Bitt eine Zahl größer oder gleich 0 eingeben.")


@view_config(
    route_name="dashboard/roles/show",
    renderer="../templates/dashboard/organizations/roles/show.mako",
    permission="edit",
)
def show(request):
    form = RoleForm(request.POST, request.context)
    if request.method == "POST" and form.validate():
        form.populate_obj(request.context)
        request.session.flash("Gespeichert.")
        return HTTPFound(
            location=request.route_path(
                "dashboard/organizations/show", id=request.context.organization.id
            )
        )

    return dict(role=request.context, form=form)


@view_config(
    route_name="dashboard/roles/new",
    renderer="../templates/dashboard/organizations/roles/new.mako",
    permission="edit",
)
def new(request):
    form = RoleForm(request.POST)
    if request.method == "POST" and form.validate():
        role = Role(organization=request.context)
        form.populate_obj(role)
        request.session.flash("Gespeichert.")
        return HTTPFound(
            location=request.route_path(
                "dashboard/organizations/show", id=request.context.id
            )
        )

    return dict(organization=request.context, form=form)
