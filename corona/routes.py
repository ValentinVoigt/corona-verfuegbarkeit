def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)

    # Statische Seiten
    config.add_route('home', '/')
    config.add_route('imprint', '/impressum')

    # Login, Logout, Registrieren, ...
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('register', '/registrieren')

    # Dashboard
    config.add_route('dashboard/organizations', '/login/organisationen')
