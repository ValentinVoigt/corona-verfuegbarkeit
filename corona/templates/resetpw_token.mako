<%inherit file="layout.mako"/>

<%namespace file="functions/field.mako" import="field"/>

<form class="form-signin" action="${request.route_path('resetpw/token', token=request.matchdict['token'])}" method="POST">
    <h1 class="h3 mb-3 font-weight-normal">Passwort zurücksetzen</h1>

    % if ok:
        <div class="alert alert-success">
            <p><b>Passwort geändert!</b></p>
            <p class="card-text">
                Wir haben dein Passwort nun geändert.
            </p>
        </div>
    % else:
        <p>
            Bitte gib nun ein neues Passwort ein.
        </p>

        ${field(form.password)}
        ${field(form.password_again)}

        <button class="btn btn-lg btn-primary btn-block" type="submit">
            Passwort setzen
        </button>
    % endif
</form>
