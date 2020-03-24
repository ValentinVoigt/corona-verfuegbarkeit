<%inherit file="../../base.mako"/>
<%namespace file="../../../functions/field.mako" import="field"/>

<div class="container">
    <nav aria-label="breadcrumb">
	<ol class="breadcrumb">
	    <li class="breadcrumb-item">
		<a href="${request.route_path('dashboard/organizations')}">Organisationen</a>
	    </li>
	    <li class="breadcrumb-item">
		<a href="${request.route_path('dashboard/organizations/show', id=organization.id)}">
		    ${organization.name}
		</a>
	    </li>
	    <li class="breadcrumb-item active" aria-current="page">
		Neue Mitglieder
	    </li>
	</ol>
    </nav>

    <h1>Neue Mitglieder</h1>

    <p>
	Hier kannst du viele Mitglieder auf einmal anlegen. Einfach eine E-Mail-Adresse pro
	Zeile eintippen. Keine Kommas oder andere Trennzeichen.
    </p>

    <form method="POST" action="${request.route_path('dashboard/users/new-batch', id=organization.id)}">
	<div class="form-group">
	    ${field(form.emails, rows=25)}
	</div>
	<input type="submit" value="Speichern" class="btn btn-primary" />
    </form>
</div>
