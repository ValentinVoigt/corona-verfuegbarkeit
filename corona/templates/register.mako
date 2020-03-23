<%inherit file="layout.mak"/>

<%namespace file="functions/field.mako" import="field"/>

<div class="container">
    <h1>Neue Organisation erstellen</h1>

    <p>
	Hier kannst du dich registrieren, um deine erste Organisation anzulegen.
	Von dort aus kannst du dann Mitarbeiter hinzufügen.
    </p>

    <p>
	Wir fragen nur nach Daten, von denen wir glauben, dass sie dir helfen. Wir
	geben grundsätzlich keine Daten an andere weiter.
    </p>

    % if success:
	<div class="alert alert-success">
	    <p><b>Deine Organisation wurde erfolgreich angelegt!</b></p>
	    <p class="card-text">
		Bitte bestätigte nun noch deine E-Mail-Adresse. Du hast hierfür einen
		Link per E-Mail erhalten. (Nicht wirklich, aber kommt noch)
	    </p>
	</div>
    % else:
	<p>
	    Pflichtfelder sind <b>fett und mit Sternchen*</b> markiert.
	</p>

	<form method="POST" action="${request.route_path('register')}">
	    <h2>Persönliche Angaben</h2>
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
	    <div class="form-row">
		<div class="form-group col-md-6">
		    ${field(form.password)}
		</div>
		<div class="form-group col-md-6">
		    ${field(form.password_again)}
		</div>
	    </div>

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

	    <button type="submit" class="btn btn-primary btn-lg">
		Organisation anlegen!
	    </button>
	</form>
    % endif
</div>
