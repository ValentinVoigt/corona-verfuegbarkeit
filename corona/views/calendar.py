from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from wtforms import SelectField, validators, DateField, ValidationError

from ..utils.form import Form

class CalendarForm(Form):
    start = DateField("Von")
    end = DateField("Bis")
    status = SelectField("Status")


@view_config(
    route_name="dashboard/calendar",
    renderer="../templates/dashboard/calendar.mako",
    # TODO ??
    # permission="group:all",
)
def calendar(request):
    form = CalendarForm()
    #form.status.choices = 


    return dict()
