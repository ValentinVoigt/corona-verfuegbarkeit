from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from wtforms import StringField, SelectField, validators, DateField, ValidationError
from datetime import date

from ..utils.form import Form
from ..models import CalendarEntry


class NameForm(Form):
    first_name = StringField("Vorname", [validators.InputRequired()])
    last_name = StringField("Nachname", [validators.InputRequired()])


class CalendarForm(Form):
    start = DateField("Von", validators=[validators.InputRequired()])
    end = DateField("Bis", validators=[validators.InputRequired()])
    status = SelectField("Status", coerce=int, validators=[validators.InputRequired()])

    def validate_start(form, field):
        start = form.start.data
        end = form.end.data
        if end:
            if end < date.today():
                raise ValidationError(
                    "Eingaben für die Vergangenheit sind nicht möglich"
                )
        if start and end:
            for entry in form.has_user.calendar:
                if (
                    entry.start <= start < entry.end
                    or entry.start < end <= entry.end
                    or start <= entry.start <= end
                ):
                    raise ValidationError(
                        "Eingabe überschneidet sich mit vorhandenen Einträgen."
                    )


@view_config(
    route_name="dashboard/calendar",
    renderer="../templates/dashboard/calendar.mako",
    permission="calendar",
)
def calendar(request):
    calendar_form = None
    name_form = None
    has_name = all([request.user.first_name, request.user.last_name])

    has_user = request.context
    organization = has_user.organization

    if not has_name:
        name_form = NameForm(request.POST, request.user)
        if request.method == "POST" and name_form.validate():
            name_form.populate_obj(request.user)
            request.session.flash("Dein Name wurden gespeichert.")
            return HTTPFound(request.route_path("dashboard/calendar", id=has_user.id))
    else:
        calendar_form = CalendarForm(
            request.POST,
            start=max([e.end for e in has_user.calendar] or [date.today()]),
        )
        calendar_form.has_user = has_user
        calendar_form.status.choices = [
            (status.id, status.name) for org, status in organization.recursive_statuses
        ]
        if request.method == "POST" and calendar_form.validate():
            request.dbsession.add(
                CalendarEntry(
                    start=calendar_form.start.data,
                    end=calendar_form.end.data,
                    calendar_entry_status_id=calendar_form.status.data,
                    organization_has_user=has_user,
                )
            )
            request.session.flash("Neuer Kalendereintrag wurde hinzugefügt.")
            return HTTPFound(request.route_path("dashboard/calendar", id=has_user.id))

    return dict(
        calendar_form=calendar_form,
        name_form=name_form,
        has_user=has_user,
        organization=organization,
        has_name=has_name,
    )


@view_config(
    route_name="dashboard/calendar/delete", permission="edit",
)
def delete(request):
    request.dbsession.delete(request.context)
    request.session.flash("Kalendereintrag wurde gelöscht.")
    return HTTPFound(
        request.route_path(
            "dashboard/calendar", id=request.context.organization_has_user.id
        )
    )
