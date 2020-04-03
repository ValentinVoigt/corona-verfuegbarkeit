from datetime import datetime
from pyramid.security import Allow

import bcrypt

from .models import User


def hash_password(pw):
    pwhash = bcrypt.hashpw(pw.encode("utf8"), bcrypt.gensalt())
    return pwhash.decode("utf8")


def check_password(pw, hashed_pw):
    expected_hash = hashed_pw.encode("utf8")
    return bcrypt.checkpw(pw.encode("utf8"), expected_hash)


def groupfinder(userid, request):
    user = request.dbsession.query(User).filter(User.email == userid).first()
    if user:
        # Solange wir noch keinen Namen haben oder die AGB noch nicht akzeptiert
        # wurden, packen wir den Nutzer nicht in seine eigene user:id-Gruppe.
        # Damit hat er noch keine Rechte auf die meisten Seiten.
        if user.agreed_tos and user.first_name and user.last_name:
            if user.needs_password and not user.password:
                return ["group:all", "group:no_password"]
            else:
                return ["group:all", "group:tos", f"user:{user.id}"]
        else:
            return ["group:all", "group:no_tos"]


def get_current_user(request):
    user = (
        request.dbsession.query(User)
        .filter(User.email == request.authenticated_userid)
        .first()
    )
    if user:
        user.last_login = datetime.now()
    return user


class RootFactory(object):
    """
    Das Wurzelobjekt für den Traversal Tree. Mit URL Dispatch nur wichtig
    um die globale ACL zu liefern.
    """

    def __init__(self, request):
        self.__acl__ = [
            (Allow, "group:tos", "loggedin"),
            (Allow, "group:no_tos", "no_tos"),
            (Allow, "group:no_password", "no_password"),
        ]


def includeme(config):
    """
    Initialize the model for a Pyramid app.

    Activate this setup using ``config.include('corona.security')``.
    """
    config.add_request_method(get_current_user, "user", reify=True)
