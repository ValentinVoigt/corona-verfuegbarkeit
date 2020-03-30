from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid_mailer.mailer import Mailer
from pyramid_mailer.message import Message
from wtforms import PasswordField, StringField, validators, ValidationError
from datetime import datetime
from pyramid.security import remember
import transaction

from ..models import Organization, User, OrganizationHasUser
from ..security import hash_password
from ..utils.form import Form
from ..utils.password import validate_password


REGISTER_SUBJECT = """Deine Anmeldung bei Corona-Verfügbarkeit"""
REGISTER_TEXT_OK = """Hallo {receiver},

du hast dich soeben bei Corona-Verfügbarkeit registriert. Bitte bestätige zum
Abschluss noch deine E-Mail-Adresse, indem du auf folgenden Link klickst:

https://www.corona-verfuegbarkeit.de/verifiziere/{token}

Vielen Dank,
Dein Team von Corona-Verfügbarkeit"""
REGISTER_TEXT_DOUBLE = """Hallo {receiver},

du hast dich soeben bei Corona-Verfügbarkeit registriert. Allerdings hast du
bereits einen Account bei uns. Ein neuer Account wurde nicht angelegt. Wenn du
dein Passwort vergessen hast, verwende die Passwort-vergessen-Funktion.
Sobald du eingeloggt bist, kannst du eine neue Organisation anlegen.

Vielen Dank,
Dein Team von Corona-Verfügbarkeit"""


class NewOrganizationForm(Form):
    organization_name = StringField(
        "Name der Organisation", [validators.InputRequired()]
    )
    organization_city = StringField("Stadt")
    organization_postal_code = StringField("Postleitzahl")


class PasswordForm(NewOrganizationForm):
    password = PasswordField(
        "Passwort", [validators.InputRequired(), validate_password]
    )
    password_again = PasswordField("Passwort (nochmal)", [validators.InputRequired()])

    def validate_password_again(form, field):
        if field.data != form.password.data:
            raise ValidationError("Die beiden Passwörter stimmen nicht überein.")


class NewUserForm(PasswordForm):
    email = StringField(
        "E-Mail-Adresse", [validators.InputRequired(), validators.Email()]
    )
    first_name = StringField("Vorname", [validators.InputRequired()])
    last_name = StringField("Nachname", [validators.InputRequired()])


@view_config(route_name="register", renderer="../templates/register.mako")
def register(request):
    if request.user and request.user.password:
        form = NewOrganizationForm(request.POST)
    elif request.user:
        form = PasswordForm(request.POST)
    else:
        form = NewUserForm(request.POST)

    error = None

    if request.method == "POST" and form.validate():
        mailer = Mailer()

        # Add user if not exists
        if request.user:
            user = request.user
        else:
            user = (
                request.dbsession.query(User)
                .filter(User.email == form.email.data)
                .first()
            )

        if not user:
            user = User(
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                password=hash_password(form.password.data),
                agreed_tos=datetime.now(),
            )
        elif request.user and not not user.password:
            user.password = hash_password(form.password.data)
        elif not request.user:
            message = Message(
                subject=REGISTER_SUBJECT,
                sender="noreply@corona-verfuegbarkeit.de",
                recipients=[user.email],
                body=REGISTER_TEXT_DOUBLE.format(receiver=user.display_name),
            )
            mailer.send(message)
            transaction.commit()
            return HTTPFound(request.route_path("register/ok"))

        # Add organization
        organization = Organization(
            name=form.organization_name.data,
            postal_code=form.organization_postal_code.data,
            city=form.organization_city.data,
        )

        # Add connection between both
        has = OrganizationHasUser(
            organization=organization, user=user, permission="owner",
        )
        request.dbsession.add(has)
        request.dbsession.flush()

        # Bereits eingeloggte Nutzer weiterleiten
        if request.user:
            return HTTPFound(
                request.route_path("dashboard/organizations/show", id=organization.id)
            )
        else:
            message = Message(
                subject=REGISTER_SUBJECT,
                sender="noreply@corona-verfuegbarkeit.de",
                recipients=[user.email],
                body=REGISTER_TEXT_OK.format(
                    receiver=user.display_name, token=user.auth_token,
                ),
            )
            mailer.send(message)
            transaction.commit()
            return HTTPFound(request.route_path("register/ok"))

    return dict(form=form, error=error)


@view_config(route_name="register/ok", renderer="../templates/registered.mako")
def register_ok(request):
    return {}


@view_config(route_name="register/verify")
def verify(request):
    user = (
        request.dbsession.query(User)
        .filter(User.auth_token == request.matchdict["token"])
        .first()
    )

    if user and user.password and not user.is_validated:
        user.is_validated = True
        user.new_token()
        headers = remember(request, user.email)
        return HTTPFound(
            location=request.route_path("dashboard/organizations"), headers=headers
        )
    else:
        return HTTPNotFound()
