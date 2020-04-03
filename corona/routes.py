def includeme(config):
    media_location = config.get_settings().get("media_location", "static")

    config.add_static_view(path="static", cache_max_age=3600, name=media_location)

    # Statische Seiten
    config.add_route("home", "/")
    config.add_route("imprint", "/impressum")

    # Login, Logout, Registrieren, ...
    config.add_route("login", "/login")
    config.add_route("login/token", "/login/{token}")
    config.add_route("resetpw", "/passwort-vergessen")
    config.add_route("resetpw/token", "/passwort-vergessen/{token}")
    config.add_route("logout", "/logout")
    config.add_route("register", "/registrieren")
    config.add_route("register/ok", "/registrieren/ok")
    config.add_route("register/verify", "/verifiziere/{token}")
    config.add_route("dashboard/tos", "/dashboard/datenschutz")
    config.add_route("dashboard/force_password", "/dashboard/passwort-setzen")

    # Organizations
    config.add_route("dashboard/organizations", "/dashboard/organisationen")
    config.add_route(
        "dashboard/organizations/show",
        "/dashboard/organisationen/{id}",
        factory="corona.models.organization.Organization._factory",
    )
    config.add_route(
        "dashboard/organizations/new",
        "/dashboard/organisationen/{id}/neu",
        factory="corona.models.organization.Organization._factory",
    )
    config.add_route(
        "dashboard/organizations/availability",
        "/dashboard/organisationen/{id}/verfuegbarkeit/{date}",
        factory="corona.models.organization.Organization._factory",
    )

    # Users
    config.add_route(
        "dashboard/users/new",
        "/dashboard/organisationen/{id}/neues-mitglied",
        factory="corona.models.organization.Organization._factory",
    )
    config.add_route(
        "dashboard/users/invite",
        "/dashboard/organisationen/{id}/mitglieder-einladen",
        factory="corona.models.organization.Organization._factory",
    )
    config.add_route(
        "dashboard/users/new-batch",
        "/dashboard/organisationen/{id}/neue-mitglieder",
        factory="corona.models.organization.Organization._factory",
    )
    config.add_route(
        "dashboard/users/show",
        "/dashboard/mitglieder/{id}",
        factory="corona.models.organization_has_user.OrganizationHasUser._factory",
    )

    # Roles
    config.add_route(
        "dashboard/roles/new",
        "/dashboard/rollen/{id}/neue",
        factory="corona.models.organization.Organization._factory",
    )
    config.add_route(
        "dashboard/roles/show",
        "/dashboard/rollen/{id}",
        factory="corona.models.role.Role._factory",
    )

    # Statuses
    config.add_route(
        "dashboard/status/new",
        "/dashboard/status/{id}/neue",
        factory="corona.models.organization.Organization._factory",
    )
    config.add_route(
        "dashboard/status/show",
        "/dashboard/status/{id}",
        factory="corona.models.status.Status._factory",
    )

    # Calendar
    config.add_route(
        "dashboard/calendar",
        "/dashboard/calendar/{id}",
        factory="corona.models.organization_has_user.OrganizationHasUser._factory",
    )
    config.add_route(
        "dashboard/calendar/delete",
        "/dashboard/calendar/loeschen/{id}",
        factory="corona.models.calendar_entry.CalendarEntry._factory",
    )
