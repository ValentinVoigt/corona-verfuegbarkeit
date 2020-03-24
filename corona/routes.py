def includeme(config):
    media_location = config.get_settings().get("media_location", "static")

    config.add_static_view(path="static", cache_max_age=3600, name=media_location)

    # Statische Seiten
    config.add_route("home", "/")
    config.add_route("imprint", "/impressum")

    # Login, Logout, Registrieren, ...
    config.add_route("login", "/login")
    config.add_route("logout", "/logout")
    config.add_route("register", "/registrieren")

    # Organizations
    config.add_route("dashboard/organizations", "/login/organisationen")
    config.add_route(
        "dashboard/organizations/show",
        "/login/organisationen/{id}",
        factory="corona.models.organization.Organization._factory",
    )

    # Users
    config.add_route(
        "dashboard/users/new",
        "/login/organisationen/{id}/neues-mitglied",
        factory="corona.models.organization.Organization._factory",
    )
    config.add_route(
        "dashboard/users/invite",
        "/login/organisationen/{id}/mitglieder-einladen",
        factory="corona.models.organization.Organization._factory",
    )
    config.add_route(
        "dashboard/users/new-batch",
        "/login/organisationen/{id}/neue-mitglieder",
        factory="corona.models.organization.Organization._factory",
    )
    config.add_route(
        "dashboard/users/show",
        "/login/mitglieder/{id}",
        factory="corona.models.organization_has_user.OrganizationHasUser._factory",
    )

    # Roles
    config.add_route(
        "dashboard/roles/new",
        "/login/rollen/{id}/neue",
        factory="corona.models.organization.Organization._factory",
    )
    config.add_route(
        "dashboard/roles/show",
        "/login/rollen/{id}",
        factory="corona.models.role.Role._factory",
    )
