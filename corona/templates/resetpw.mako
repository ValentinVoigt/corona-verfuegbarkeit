<%inherit file="layout.mako"/>

<form class="form-signin" action="${request.route_path('resetpw')}" method="POST">
    <h1 class="h3 mb-3 font-weight-normal">Passwort zurücksetzen</h1>

    % if request.method == "POST":
        <div class="alert alert-success">
            <p><b>E-Mail verschickt</b></p>
            <p class="card-text">
                Wir haben dir eine E-Mail geschickt. Dort findest du einen Link,
                um dein Passwort neu setzen zu können.
            </p>
        </div>
    % else:
        <p>
            Falls du dein Passwort vergessen hast, kannst du dir ein neues setzen.
            Gib dafür deine E-Mail-Adresse hier ein. Wir senden dir dann eine E-Mail
            mit einem Link.
        </p>
    % endif

    <label for="inputEmail" class="sr-only">E-Mail-Adresse</label>
    <input
        name="email"
        type="email"
        id="inputEmail"
        class="form-control"
        placeholder="E-Mail-Adresse"
        required
        autofocus
        % if request.method == "POST":
            disabled
        % endif
    >

    <button
        class="btn btn-lg btn-primary btn-block"
        type="submit"
        % if request.method == "POST":
            disabled
        % endif
    >
        Absenden
    </button>
</form>
