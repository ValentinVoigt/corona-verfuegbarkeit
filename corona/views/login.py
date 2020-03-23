from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from pyramid.security import remember, forget

from ..security import check_password
from ..models import User


@view_config(route_name="login", renderer="../templates/login.mako")
def login(request):
    login_url = request.route_url("login")
    referrer = request.url
    if referrer == login_url:
        referrer = "/"  # never use login form itself as came_from
    came_from = request.POST.get("came_from", referrer)

    if request.method == "POST":
        user = (
            request.dbsession.query(User)
            .filter(User.email == request.POST["login"])
            .first()
        )

        if (
            user
            and user.password
            and check_password(request.POST["password"], user.password)
        ):
            headers = remember(request, request.POST["login"])
            return HTTPFound(location=came_from, headers=headers)

    return dict(
        name="Login", url=request.application_url + "/login", came_from=came_from,
    )


@view_config(route_name="logout")
def logout(request):
    headers = forget(request)
    url = request.route_url("home")
    return HTTPFound(location=url, headers=headers)
