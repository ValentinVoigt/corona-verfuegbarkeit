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

    # Dashboard
    config.add_route("dashboard/organizations", "/login/organisationen")
