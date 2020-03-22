from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from .security import groupfinder


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

        config.include("pyramid_mako")
        config.include("pyramid_mailer")
        config.include(".models")
        config.include(".routes")
        config.include(".security")
        config.scan()

    return config.make_wsgi_app()
