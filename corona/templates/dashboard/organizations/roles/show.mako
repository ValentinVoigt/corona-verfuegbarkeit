<%inherit file="../../base.mako"/>
<%namespace file="../../../functions/field.mako" import="field"/>

<div class="container">
    <nav aria-label="breadcrumb">
	<ol class="breadcrumb">
	    <li class="breadcrumb-item">
		<a href="${request.route_path('dashboard/organizations')}">Organisationen</a>
	    </li>
	    <li class="breadcrumb-item">
		<a href="${request.route_path('dashboard/organizations/show', id=role.organization.id)}">
		    ${role.organization.name}
		</a>
	    </li>
	    <li class="breadcrumb-item active" aria-current="page">
		${role.name}
	    </li>
	</ol>
    </nav>

    <h1>Rolle: ${role.name}</h1>

    <form method="POST" action="${request.route_path('dashboard/roles/show', id=role.organization.id)}">
	<div class="form-group">
	    ${field(form.name)}
	</div>
	<div class="form-group">
	    ${field(form.color, type="color")}
	</div>
	<div class="form-group">
	    ${field(form.minimum_required)}
	</div>
	<input type="submit" value="Speichern" class="btn btn-primary" />
    </form>
</div>


