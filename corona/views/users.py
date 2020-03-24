from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from wtforms import (
    TextAreaField,
    StringField,
    SelectField,
    SelectMultipleField,
    validators,
    ValidationError,
)

from ..utils.form import Form
from ..models import OrganizationHasUser, User, Role

import re


INVITE_EMAIL = """Hallo {receiver},

{sender} bittet dich, dich bei Corona-Verfügbarkeit anzumelden und deine Verfügbarkeit für die Organisation {organization} anzugeben.

Melde dich jetzt an: www.corona-verfügbarkeit.de/login/{token}

Vielen Dank, dein Team von Corona-Verfügbarkeit"""


def validate_email(email):
    regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    return bool(regex.match(email))


def split_emails(data):
    return list(set([e.strip().lower() for e in re.split("\t|\n|,|;| ", data.strip())]))


class UserForm(Form):
    email = StringField(
        "E-Mail-Adresse", [validators.InputRequired(), validators.Email()]
    )
    first_name = StringField("Vorname")
    last_name = StringField("Nachname")


class UserDetailsForm(UserForm):
    permission = SelectField(
        "Zugriffsrechte",
        choices=[
            ("owner", "Eigentümer (darf alles, auch Organisation löschen)"),
            ("admin", "Administrator (darf alles, außer Organisation löschen)"),
            ("auditor", "Prüfer (darf alles einsehen, aber nicht verändern)"),
            ("member", "Mitglied (Darf nur seine eigenen Informationen bearbeiten"),
        ],
        validators=[validators.InputRequired()],
    )
    roles = SelectMultipleField("Rollen", coerce=int)


class UserBatchForm(Form):
    emails = TextAreaField("E-Mail-Adressen", [validators.InputRequired()])

    def validate_emails(form, field):
        emails = split_emails(field.data)
        for email in emails:
            if not validate_email(email):
                raise ValidationError(
                    f'Bitte nur E-Mail-Adressen eingeben ("{email}").'
                )


@view_config(
    route_name="dashboard/users/show",
    renderer="../templates/dashboard/organizations/users/show.mako",
    permission="edit",
)
def show(request):
    form = UserDetailsForm(request.POST, request.context.user)
    form.roles.choices = [
        (r.id, r.name) for (o, r) in request.context.organization.recursive_roles
    ]
    if request.method == "POST" and form.validate():
        form.populate_obj(request.context.user)
        request.context.roles = [
            request.dbsession.query(Role).get(i) for i in form.roles.data
        ]
        request.session.flash("Gespeichert.")
    return dict(has_user=request.context, form=form)


@view_config(
    route_name="dashboard/users/new",
    renderer="../templates/dashboard/organizations/users/new.mako",
    permission="edit",
)
def new(request):
    form = UserForm(request.POST)
    if request.method == "POST" and form.validate():
        if request.context.has_user(form.email.data):
            request.session.flash("Mitglied mit dieser E-Mail-Adresse existiert schon.")
        else:
            user = User()
            form.populate_obj(user)
            has_user = OrganizationHasUser(organization=request.context, user=user)
            request.dbsession.flush()
            request.session.flash("Neues Mitglied wurde hinzugefügt")

            return HTTPFound(
                location=request.route_path("dashboard/users/show", id=has_user.id)
            )

    return dict(organization=request.context, form=form)


@view_config(
    route_name="dashboard/users/new-batch",
    renderer="../templates/dashboard/organizations/users/new-batch.mako",
    permission="edit",
)
def new_batch(request):
    form = UserBatchForm(request.POST)

    if request.method == "POST" and form.validate():
        emails = split_emails(form.emails.data)
        num = 0
        for email in emails:
            if not request.context.has_user(email):
                user = User(email=email)
                has_user = OrganizationHasUser(organization=request.context, user=user)
                num += 1

        request.session.flash(f"{num} neue Mitglieder hinzugefügt")

        return HTTPFound(
            location=request.route_path(
                "dashboard/organizations/show", id=request.context.id
            )
        )

    return dict(organization=request.context, form=form)


@view_config(
    route_name="dashboard/users/invite",
    renderer="../templates/dashboard/organizations/users/invite.mako",
    permission="edit",
)
def invite(request):
    text = INVITE_EMAIL.format(
        receiver="Max Mustermann",
        sender=request.user.display_name,
        organization=request.context.display_name,
        token="asd",
    )

    if request.method == "POST" and form.validate():
        return HTTPFound(
            location=request.route_path(
                "dashboard/organizations/show", id=request.context.id
            )
        )

    return dict(organization=request.context, text=text, num=0,)
