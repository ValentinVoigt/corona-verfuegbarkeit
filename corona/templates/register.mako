<%inherit file="layout.mako"/>

<%namespace file="functions/field.mako" import="field"/>

<div class="container">
    <h1>Neue Organisation erstellen</h1>

    % if not request.user:
        <p>
            Hier kannst du dich registrieren, um deine erste Organisation anzulegen.
            Von dort aus kannst du dann Mitarbeiter hinzufügen.
        </p>

        <p>
            Wir fragen nur nach Daten, von denen wir glauben, dass sie dir helfen. Wir
            geben grundsätzlich keine Daten an andere weiter.
        </p>
    % else:
        <p>
            Du bist bereits als <strong>${request.user.display_name}</strong> eingeloggt. Hier
            kannst du eine weitere Organisation anlegen.  Falls du Unterorganisationen
            anlegen möchtest, verwende bitte den Button <i>Unterorganisation anlegen</i>
            in der <a href="${request.route_path('dashboard/organizations')}">Organisationsübersicht</a>.
        </p>

        % if not request.user.password:
            <p>
                Als Eigentümer einer Organisation musst du dir außerdem ein Passwort setzen.
            </p>
        % endif
    % endif

    <p>
        Pflichtfelder sind <b>fett und mit Sternchen*</b> markiert.
    </p>

    <form method="POST" action="${request.route_path('register')}">
        % if not request.user or not request.user.password:
            <h2>Persönliche Angaben</h2>
            % if not request.user:
                <div class="form-row">
                    <div class="form-group col-md-6">
                        ${field(form.first_name)}
                    </div>
                    <div class="form-group col-md-6">
                        ${field(form.last_name)}
                    </div>
                </div>
                <div class="form-group">
                    ${field(form.email)}
                </div>
            % endif
            <div class="form-row">
                <div class="form-group col-md-6">
                    ${field(form.password)}
                </div>
                <div class="form-group col-md-6">
                    ${field(form.password_again)}
                </div>
            </div>
        % endif

        <h2>Angaben zur Organisation</h2>
        <div class="form-group">
            ${field(form.organization_name)}
        </div>
        <div class="form-row">
            <div class="form-group col-md-6">
                ${field(form.organization_postal_code)}
            </div>
            <div class="form-group col-md-6">
                ${field(form.organization_city)}
            </div>
        </div>

        <p class="text-right mt-3">
            <button type="submit" class="btn btn-primary btn-lg">
                Organisation anlegen!
            </button>
        </p>
    </form>
</div>
