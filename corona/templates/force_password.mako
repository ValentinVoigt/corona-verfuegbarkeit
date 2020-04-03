<%inherit file="layout.mako"/>

<%namespace file="functions/field.mako" import="field"/>

<form class="form-signin" action="" method="POST">
    <h1 class="h3 mb-3 font-weight-normal">Passwort setzen</h1>

    <p>
        Du hast auf mindestens eine Organisation Leserechte und musst daher
        ein Passwort setzen.
    </p>
    <p>
        Bitte gib nun ein Passwort ein.
    </p>

    ${field(form.password)}
    ${field(form.password_again)}

    <button class="btn btn-lg btn-primary btn-block" type="submit">
        Passwort setzen
    </button>
</form>
