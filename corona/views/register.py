from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from wtforms import Form, PasswordField, StringField, validators, ValidationError
from datetime import datetime

from ..models import Organization, User, OrganizationHasUser
from ..security import hash_password


class NewOrganizationForm(Form):
    organization_name = StringField(
        "Name der Organisation", [validators.InputRequired()]
    )
    organization_city = StringField("Stadt")
    organization_postal_code = StringField("Postleitzahl")


class PasswordForm(NewOrganizationForm):
    password = PasswordField("Passwort", [validators.InputRequired()])
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
    success = False

    if request.method == "POST" and form.validate():
        # Add user if not exists
        if request.user:
            user = request.user
            is_double_registration = False
        else:
            user = (
                request.dbsession.query(User)
                .filter(User.email == form.email.data)
                .first()
            )
            is_double_registration = bool(user)

        if not user:
            user = User(
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                password=hash_password(form.password.data),
                agreed_tos=datetime.now(),
            )
        else:
            if not user.password:
                user.password = hash_password(form.password.data)

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

        # Show success message
        success = True

    return dict(form=form, error=error, success=success)
