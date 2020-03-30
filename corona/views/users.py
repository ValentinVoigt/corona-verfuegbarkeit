from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid_mailer.mailer import Mailer
from pyramid_mailer.message import Message
from datetime import datetime
from wtforms import (
    TextAreaField,
    StringField,
    SelectField,
    BooleanField,
    validators,
    ValidationError,
)

from ..utils.form import Form
from ..models import User, OrganizationHasUser

import transaction
import re

INVITE_EMAIL_SUBJECT = """Deine Verfügbarkeit für {organization}"""
INVITE_EMAIL_TEXT = """Hallo {receiver},

{sender} bittet dich, dich bei Corona-Verfügbarkeit anzumelden und deine
Verfügbarkeit für die Organisation {organization} anzugeben.

Melde dich jetzt an: https://www.corona-verfuegbarkeit.de/login/{token}

Vielen Dank,
Dein Team von Corona-Verfügbarkeit"""


def validate_email(email):
    regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    return bool(regex.match(email))


def split_emails(data):
    # E-Mails raussuchen
    emails = [e.strip().lower() for e in re.split("\t|\n|,|;| ", data.strip())]
    # Leere entfernen
    emails = list(filter(lambda e: bool(e), emails))
    # Unique machen
    emails = list(set(emails))
    return emails


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
    # Erstelle neues Formular mit BooleanField für jede Rolle
    class DynamicUserDetailsForm(UserDetailsForm):
        pass

    for org, role in request.context.organization.recursive_roles:
        setattr(
            DynamicUserDetailsForm,
            f"role_{role.id}",
            BooleanField(role.name, default=role.id in request.context.role_ids),
        )

    # Hole bestehende Daten
    default_data = {
        "email": request.context.user.email,
        "first_name": request.context.user.first_name,
        "last_name": request.context.user.last_name,
        "permission": request.context.permission,
    }

    # Form-Behandlung
    form = DynamicUserDetailsForm(request.POST, **default_data)

    if request.method == "POST" and form.validate():
        request.context.user.email = form.email.data
        request.context.user.first_name = form.first_name.data
        request.context.user.last_name = form.last_name.data
        request.context.permission = form.permission.data

        request.context.roles = list(
            filter(
                lambda role: getattr(form, f"role_{role.id}").data,
                [role for org, role in request.context.organization.recursive_roles],
            )
        )

        request.session.flash("Gespeichert.")
        return HTTPFound(
            location=request.route_path(
                "dashboard/organizations/show", id=request.context.organization.id
            )
        )

    return dict(has_user=request.context, form=form)


@view_config(
    route_name="dashboard/users/new",
    renderer="../templates/dashboard/organizations/users/new.mako",
    permission="edit",
)
def new(request):
    form = UserForm(request.POST)
    if request.method == "POST" and form.validate():
        if form.email.data.lower() in [
            h.user.email.lower() for h in request.context.has_users
        ]:
            request.session.flash("Mitglied mit dieser E-Mail-Adresse existiert schon.")
        else:
            existing_user = (
                request.dbsession.query(User)
                .filter(User.email == form.email.data)
                .first()
            )
            if existing_user:
                user = existing_user
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
            user_in_org = False
            for has_user in request.context.has_users:
                if has_user.user.email.lower() == email.lower():
                    user_in_org = True
                    break
            if not user_in_org:
                existing_user = (
                    request.dbsession.query(User).filter(User.email == email).first()
                )
                if existing_user:
                    user = existing_user
                else:
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
    subject = INVITE_EMAIL_SUBJECT.format(organization=request.context.display_name)
    text = INVITE_EMAIL_TEXT.format(
        receiver=request.user.display_name,
        sender=request.user.display_name,
        organization=request.context.display_name,
        token="diesisteinbeispiel",
    )

    if request.method == "POST":
        mailer = Mailer()
        for user in request.context.uninvited_users:
            user.ensure_token_exists()
            user.last_invite = datetime.now()
            message = Message(
                subject=INVITE_EMAIL_SUBJECT.format(
                    organization=request.context.display_name
                ),
                sender="noreply@corona-verfuegbarkeit.de",
                recipients=[user.email],
                body=INVITE_EMAIL_TEXT.format(
                    receiver=user.display_name,
                    sender=request.user.display_name,
                    organization=request.context.display_name,
                    token=user.auth_token,
                ),
            )

            mailer.send(message)

        request.session.flash(
            f"{len(request.context.uninvited_users)} Mails verschickt!"
        )
        transaction.commit()

        return HTTPFound(
            location=request.route_path(
                "dashboard/organizations/show", id=request.context.id
            )
        )

    return dict(
        organization=request.context,
        text=text,
        subject=subject,
        num=len(request.context.uninvited_users),
    )
