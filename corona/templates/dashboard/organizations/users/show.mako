<%inherit file="../../base.mako"/>
<%namespace file="../../../functions/field.mako" import="field"/>

<div class="container">
    <nav aria-label="breadcrumb">
	<ol class="breadcrumb">
	    <li class="breadcrumb-item">
		<a href="${request.route_path('dashboard/organizations')}">Organisationen</a>
	    </li>
	    <li class="breadcrumb-item">
		<a href="${request.route_path('dashboard/organizations/show', id=has_user.organization.id)}">
		    ${has_user.organization.name}
		</a>
	    </li>
	    <li class="breadcrumb-item active" aria-current="page">
		${has_user.user.display_name}
	    </li>
	</ol>
    </nav>

    <h1>${has_user.user.display_name}</h1>

    <form method="POST" action="${request.route_path('dashboard/users/show', id=has_user.id)}">
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
	<div class="form-group">
	    ${field(form.permission)}
	</div>
	<div class="form-group">
	    ${field(form.roles)}
	    <p>Halte die Strg-Taste gedrückt, um mehrere Rollen auszuwählen.</p>
	</div>
	<input type="submit" value="Speichern" class="btn btn-primary" />
    </form>
</div>

