from datetime import datetime

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
        return ["group:all", f"user:{user.id}"]


def get_current_user(request):
    user = (
        request.dbsession.query(User)
        .filter(User.email == request.authenticated_userid)
        .first()
    )
    if user:
        user.last_login = datetime.now()
    return user


def includeme(config):
    """
    Initialize the model for a Pyramid app.

    Activate this setup using ``config.include('corona.security')``.
    """
    config.add_request_method(get_current_user, "user", reify=True)
