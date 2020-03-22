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
        return ["g:all"]


def includeme(config):
    """
    Initialize the model for a Pyramid app.

    Activate this setup using ``config.include('corona.security')``.
    """
    config.add_request_method(
        lambda r: r.dbsession.query(User)
        .filter(User.email == r.authenticated_userid)
        .first(),
        "user",
        reify=True,
    )
