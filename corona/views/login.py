from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.view import view_config
from pyramid.security import remember, forget
from pyramid_mailer.mailer import Mailer
from pyramid_mailer.message import Message
from datetime import datetime
from wtforms import PasswordField, validators, ValidationError
import transaction

from ..security import check_password, hash_password
from ..models import User
from ..utils.form import Form
from ..utils.password import validate_password


RESETPW_SUBJECT = """Dein Passwort bei Corona-Verfügbarkeit"""
RESETPW_TEXT = """Hallo {receiver},

du hast soeben bei Corona-Verfügbarkeit auf Passwort vergessen geklickt. Falls
du das nicht nicht warst, kannst du diese E-Mail einfach ignorieren. Ansonsten
klicke auf folgenden Link, um dein Passwort zurückzusetzen:

https://www.corona-verfuegbarkeit.de/passwort-vergessen/{token}

Vielen Dank,
Dein Team von Corona-Verfügbarkeit"""


class PasswordForm(Form):
    password = PasswordField(
        "Passwort", [validators.InputRequired(), validate_password]
    )
    password_again = PasswordField("Passwort (nochmal)", [validators.InputRequired()])

    def validate_password_again(form, field):
        if field.data != form.password.data:
            raise ValidationError("Die beiden Passwörter stimmen nicht überein.")


@view_config(route_name="login", renderer="../templates/login.mako")
def login(request):
    if request.method == "POST":
        user = (
            request.dbsession.query(User)
            .filter(User.email == request.POST["login"])
            .first()
        )

        if (
            user
            and user.password
            and user.is_validated
            and check_password(request.POST["password"], user.password)
        ):
            headers = remember(request, request.POST["login"])
            return HTTPFound(
                location=request.route_path("dashboard/organizations"), headers=headers
            )

    return dict()


@view_config(route_name="login/token", renderer="../templates/login.mako")
def login_token(request):
    user = (
        request.dbsession.query(User)
        .filter(User.auth_token == request.matchdict["token"])
        .first()
    )

    if user and not user.password:
        user.is_validated = True
        headers = remember(request, user.email)
        if user.agreed_tos:
            if len(user.has_organizations) > 0:
                return HTTPFound(
                    location=request.route_path(
                        "dashboard/calendar", id=user.has_organizations[0].id
                    ),
                    headers=headers,
                )
            else:
                return HTTPFound(
                    location=request.route_path("dashboard/organizations"),
                    headers=headers,
                )
        else:
            return HTTPFound(
                location=request.route_path("dashboard/tos"), headers=headers
            )

    return dict(
        error_message=(
            "Bitte nutze deine E-Mail-Adresse und dein Passwort zum Einloggen."
        )
    )


@view_config(route_name="dashboard/tos", renderer="../templates/tos.mako")
def tos(request):
    if request.method == "POST" and request.POST["agrees"] == "yes":
        request.user.agreed_tos = datetime.now()
        if len(request.user.has_organizations) > 0:
            return HTTPFound(
                location=request.route_path(
                    "dashboard/calendar", id=request.user.has_organizations[0].id
                )
            )
        else:
            return HTTPFound(location=request.route_path("dashboard/organizations"))

    return dict()


@view_config(route_name="logout")
def logout(request):
    headers = forget(request)
    url = request.route_url("home")
    return HTTPFound(location=url, headers=headers)


@view_config(route_name="resetpw", renderer="../templates/resetpw.mako")
def resetpw(request):
    if request.method == "POST":
        mailer = Mailer()
        user = (
            request.dbsession.query(User)
            .filter(User.email == request.POST["email"])
            .first()
        )
        if user:
            message = Message(
                subject=RESETPW_SUBJECT,
                sender="noreply@corona-verfuegbarkeit.de",
                recipients=[user.email],
                body=RESETPW_TEXT.format(
                    receiver=user.display_name, token=user.auth_token,
                ),
            )
            mailer.send(message)
            transaction.commit()

    return {}


@view_config(route_name="resetpw/token", renderer="../templates/resetpw_token.mako")
def resetpw_token(request):
    user = (
        request.dbsession.query(User)
        .filter(User.auth_token == request.matchdict["token"])
        .first()
    )

    if user:
        user.is_validated = True
        form = PasswordForm(request.POST)
        if request.method == "POST" and form.validate():
            user.password = hash_password(form.password.data)
            user.new_token()
            ok = True
        else:
            ok = False

        return dict(ok=ok, form=form)
    else:
        return HTTPNotFound()
