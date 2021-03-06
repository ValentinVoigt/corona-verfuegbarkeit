from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.session import SignedCookieSessionFactory

from .security import groupfinder, RootFactory


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        # Security policies
        authn_policy = AuthTktAuthenticationPolicy(
            settings["cookie_secret"], callback=groupfinder, hashalg="sha512"
        )
        authz_policy = ACLAuthorizationPolicy()
        config.set_authentication_policy(authn_policy)
        config.set_authorization_policy(authz_policy)
        config.set_root_factory(RootFactory)

        # Session
        my_session_factory = SignedCookieSessionFactory(
            settings["cookie_secret"], httponly=True
        )
        config.set_session_factory(my_session_factory)

        # Includes
        config.include("pyramid_mako")
        config.include(".models")
        config.include(".routes")
        config.include(".security")
        config.scan()

    return config.make_wsgi_app()
