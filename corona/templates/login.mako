<%inherit file="layout.mako"/>

<form class="form-signin" action="${request.route_path('login')}" method="POST">
    <h1 class="h3 mb-3 font-weight-normal">Einloggen</h1>

    % if request.method == "POST":
        <div class="alert alert-danger">
            <p><b>Login fehlgeschlaten</b></p>
            <p class="card-text">Der Login war leider nicht möglich. Stimmen Benutzername und Passwort?</p>
        </div>
    % endif
    % if error_message:
        <div class="alert alert-danger">
            ${error_message}
        </div>
    % endif

    <label for="inputEmail" class="sr-only">E-Mail-Adresse</label>
    <input
        name="login"
        type="email"
        id="inputEmail"
        class="form-control"
        placeholder="E-Mail-Adresse"
        required
        autofocus
    >

    <label for="inputPassword" class="sr-only">Passwort</label>
    <input
        name="password"
        type="password"
        id="inputPassword"
        class="form-control"
        placeholder="Passwort"
        required
    >

    <div class="checkbox mb-3">
        <label>
            <input type="checkbox" value="remember-me"> Eingeloggt bleiben
        </label>
    </div>

    <button class="btn btn-lg btn-primary btn-block" type="submit">
        Einloggen
    </button>

    <p class="mt-3 mb-0">
        <a href="#">
            Passwort vergessen?
        </a>
    </p>
</form>
